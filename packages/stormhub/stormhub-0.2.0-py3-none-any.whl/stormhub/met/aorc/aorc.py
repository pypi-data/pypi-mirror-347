"""AORC Item class."""

import datetime
import json
import logging
import os
from typing import Any

import numpy as np
import s3fs
import xarray as xr
from affine import Affine
from matplotlib import patches
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from pyproj import CRS
from pystac import Asset, Item, MediaType
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.storage import CloudPlatform, StorageExtension
from shapely import Polygon, to_geojson
from shapely.geometry import shape

from stormhub.met.transpose import Transpose

NULL_POLYGON = Polygon()

from stormhub.met.consts import (
    AORC_PRECIP_VARIABLE,
    AORC_X_VAR,
    AORC_Y_VAR,
    MM_TO_INCH_CONVERSION_FACTOR,
    NOAA_AORC_S3_BASE_URL,
)


class AORCItem(Item):
    """Initialize an AORC Item.

    Args:
        item_id (str): The ID of the item.
        start_datetime (datetime.datetime): The AORC start datetime.
        duration_hours (int): Duration of AORC data in hours.
        watershed (str): Location of watershed geometry geojson.
        transposition_domain (str): Location of transposition domain geometry geojson.
        local_directory (str): Local directory path
        watershed_name (str, optional): Name of watershed.
        transposition_domain_name (str, optional): Name of transposition name.
        **kwargs (Any): Additional keyword arguments.
    """

    def __init__(
        self,
        item_id: str,
        start_datetime: datetime.datetime,
        duration_hours: int,
        watershed: str,
        transposition_domain: str,
        local_directory: str,
        watershed_name: str = None,
        transposition_domain_name: str = None,
        **kwargs: Any,
    ):
        self.item_id = item_id
        self.duration_hours = f"{duration_hours}hrs"
        self.duration = duration_hours
        if not watershed_name:
            self.watershed_name = os.path.basename(watershed).replace(".geojson", "")
        else:
            self.watershed_name = watershed_name

        if not transposition_domain_name:
            self.transposition_domain_name = os.path.basename(transposition_domain).replace(".geojson", "")
        else:
            self.transposition_domain_name = transposition_domain_name

        self.watershed_geometry = watershed
        self.transposition_domain_geometry = transposition_domain
        self.local_directory = local_directory

        self.properties = kwargs.get("properties", {})
        self.stac_extensions = kwargs.get("stac_extensions", None)
        self.href = kwargs.get("href", None)
        self.collection = kwargs.get("collection", None)
        self.extra_fields = kwargs.get("extra_fields", None)
        self.assets = kwargs.get("assets", None)
        self.fiona_env_kwargs = {
            k: v
            for k, v in kwargs.items()
            if k not in ["properties", "stac_extensions", "href", "collection", "extra_fields", "assets"]
        }

        self.start_datetime = start_datetime
        self.end_datetime = start_datetime + self.duration
        super().__init__(
            self.item_id,
            NULL_POLYGON,
            self.transposition_domain_geometry.bounds,
            self.start_datetime,
            self.properties,
            self.start_datetime,
            self.end_datetime,
            self.stac_extensions,
            self.href,
            self.collection,
            self.extra_fields,
            self.assets,
        )

        self._register_extensions()
        self._aorc_source_data: xr.Dataset | None = None
        self._aorc_paths: list[str] | None = None
        self._transpose: Transpose | None = None
        self._sum_aorc: xr.DataArray | None = None
        self._transposed_watershed: Polygon | None = None
        self._transposition_transform: Affine | None = None
        self._stats: dict | None = None

    def _register_extensions(self) -> None:
        """Register item extensions."""
        ProjectionExtension.add_to(self)
        StorageExtension.add_to(self)

    @property
    def aorc_paths(self) -> list[str]:
        """Construct s3 paths for AORC datasets for given start time and duration."""
        if self._aorc_paths is None:
            if self.end_datetime.year == self.start_datetime.year:
                self._aorc_paths = [f"{NOAA_AORC_S3_BASE_URL}/{self.start_datetime.year}.zarr"]
            else:
                year_list = []
                current_year = self.start_datetime.year
                while current_year <= self.end_datetime.year:
                    year_list.append(current_year)
                    current_year += 1
                self._aorc_paths = [f"{NOAA_AORC_S3_BASE_URL}/{year}.zarr" for year in year_list]
            logging.debug("year_list for %s: %s", self.start_datetime, self._aorc_paths)
        return self._aorc_paths

    @property
    def aorc_source_data(self) -> xr.Dataset:
        """Extract AORC source data.

        - reads AORC data into memory as multifile dataset using s3 paths
        - doesn't read the entire ZARR files, instead just reads slice of data corresponding to transposition domain geometry and limited to start and end time
        - adds ZARR files to assets if they don't exist already
        """
        if self._aorc_source_data is None:
            s3_out = s3fs.S3FileSystem(anon=True)
            fileset = [s3fs.S3Map(root=aorc_path, s3=s3_out, check=False) for aorc_path in self.aorc_paths]
            ds = xr.open_mfdataset(fileset, engine="zarr", chunks="auto", consolidated=True)

            transposition_geom_for_clip = self.transposition_domain_geometry
            bounds = transposition_geom_for_clip.bounds
            # adjust start slice to make sure start datetime is exclusive minimum (get data > start not data >= start)
            start_timeslice_value = self.start_datetime + datetime.timedelta(hours=1)
            subsection = ds.sel(
                time=slice(start_timeslice_value, self.end_datetime),
                longitude=slice(bounds[0], bounds[2]),
                latitude=slice(bounds[1], bounds[3]),
            )
            self._aorc_source_data = subsection.rio.clip([transposition_geom_for_clip], drop=True, all_touched=True)
            for aorc_path in self.aorc_paths:
                aorc_year = int(os.path.basename(aorc_path).replace(".zarr", ""))
                aorc_start_datetime = datetime.datetime(
                    year=aorc_year, month=1, day=1, hour=0, tzinfo=datetime.timezone.utc
                )
                aorc_end_datetime = datetime.datetime(
                    year=aorc_year + 1, month=1, day=1, hour=0, tzinfo=datetime.timezone.utc
                )
                asset = Asset(
                    aorc_path,
                    media_type=MediaType.ZARR,
                    extra_fields={
                        "start_datetime": aorc_start_datetime.isoformat(),
                        "end_datetime": aorc_end_datetime.isoformat(),
                    },
                    roles=[MediaType.ZARR],
                )
                storage = StorageExtension.ext(asset)
                storage.platform = CloudPlatform.AWS
                self.add_asset(f"AORC_{aorc_year}", asset)

        return self._aorc_source_data

    @property
    def transpose(self) -> Transpose:
        """Create transpose class to use for transposition functions."""
        if self._transpose is None:
            watershed_geom_for_transpose = self.watershed_geometry
            self._transpose = Transpose(
                self.sum_aorc["APCP_surface"], watershed_geom_for_transpose, AORC_X_VAR, AORC_Y_VAR
            )
        return self._transpose

    @property
    def sum_aorc(self) -> xr.DataArray:
        """Sum AORC precipitation data over the duration."""
        if self._sum_aorc is None:
            self._sum_aorc = self.aorc_source_data.sum(dim="time", skipna=True, min_count=1)
        return self._sum_aorc

    @staticmethod
    def _create_stats(array: np.ndarray) -> dict:
        """Create stats from array."""
        return {
            "min": round(float(np.nanmin(array)) * MM_TO_INCH_CONVERSION_FACTOR, 2),
            "mean": round(float(np.nanmean(array)) * MM_TO_INCH_CONVERSION_FACTOR, 2),
            "max": round(float(np.nanmax(array)) * MM_TO_INCH_CONVERSION_FACTOR, 2),
            "units": "inches",
            # "sum": float(np.nansum(array)) * MM_TO_INCH_CONVERSION_FACTOR,
        }

    def max_transpose(self, add_properties: bool = True) -> tuple[Polygon, Affine, dict]:
        """Get max transpose.

        - convert max array to polygon
        - add stats object to item properties
        - record transpose centroid as item geometry
        - record max shift (as affine transform) to item properties
        - return polygon, transform, and stats
        """
        if not all([self._transposed_watershed, self._transposition_transform, self._stats]):
            self._transposed_watershed, self._transposition_transform, self._stats = self.transpose.max_transpose(
                self._create_stats
            )
        if add_properties:
            self.geometry = json.loads(to_geojson(self._transposed_watershed.centroid))
            self.properties["aorc:statistics"] = self._stats
            self.properties["aorc:transform"] = {
                "a": self._transposition_transform.a,
                "b": self._transposition_transform.b,
                "c": self._transposition_transform.c,
                "d": self._transposition_transform.d,
                "e": self._transposition_transform.e,
                "f": self._transposition_transform.f,
            }
        return (
            self._transposed_watershed,
            self._transposition_transform,
            self._stats,
            self._transposed_watershed.centroid,
        )

    def aorc_thumbnail(
        self,
        scale_max: float,
        add_asset: bool = True,
        write: bool = True,
        return_fig: bool = False,
    ) -> Figure:
        """Create AORC STAC item thumbnail.

        Creates matplotlib figure showing:
        - location of transposed watershed with maximum precip accumulation
        - original location of watershed
        - valid area of transposition
        - original transposition domain
        """
        if self._transposed_watershed is None:
            self._transposed_watershed, self._transposition_transform, self._stats = self.transpose.max_transpose(
                self._create_stats
            )
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.set_facecolor("w")
        colormap = plt.get_cmap("Spectral_r")
        (self.sum_aorc["APCP_surface"] * MM_TO_INCH_CONVERSION_FACTOR).plot(
            ax=ax, cmap=colormap, cbar_kwargs={"label": "Accumulation (Inches)"}, vmin=0, vmax=scale_max
        )
        valid_area_plt_polygon = patches.Polygon(
            np.column_stack(self.transpose.valid_spaces_polygon.exterior.coords.xy),
            lw=0.7,
            facecolor="none",
            edgecolor="gray",
        )
        ax.add_patch(valid_area_plt_polygon)
        watershed_plt_polygon = patches.Polygon(
            np.column_stack(self.watershed_geometry.exterior.coords.xy),
            lw=0.7,
            facecolor="none",
            edgecolor="gray",
        )
        ax.add_patch(watershed_plt_polygon)
        transposed_watershed_plt_polygon = patches.Polygon(
            np.column_stack(self._transposed_watershed.exterior.coords.xy),
            lw=1,
            facecolor="none",
            edgecolor="black",
        )
        ax.add_patch(transposed_watershed_plt_polygon)
        ax.set(title=None, xlabel=None, ylabel=None)

        if add_asset | write:
            if not os.path.isdir(self.local_directory):
                os.makedirs(self.local_directory)

            filename = f"{self.item_id}.thumbnail.png"
            fn = os.path.join(self.local_directory, filename)
            fig.savefig(fn, bbox_inches="tight")
            asset = Asset(filename, media_type=MediaType.PNG, roles=["thumbnail"])
            self.add_asset("thumbnail", asset)
        if return_fig:
            return fig
        else:
            plt.close()


def valid_spaces_item(watershed: Item, transposition_region: Item, storm_duration: int = 72) -> Polygon:
    """Search a sample zarr dataset to identify valid spaces for transposition. datetime.datetime(1980, 5, 1) is used as a start time for the search."""
    s3 = s3fs.S3FileSystem(anon=True)
    start_time = datetime.datetime(1980, 5, 1)
    sample_data = s3fs.S3Map(root=f"{NOAA_AORC_S3_BASE_URL}/{start_time.year}.zarr", s3=s3)
    ds = xr.open_dataset(sample_data, engine="zarr", chunks="auto", consolidated=True)
    bounds = shape(transposition_region.geometry).bounds

    subset = ds.sel(
        time=slice(start_time, start_time + datetime.timedelta(hours=storm_duration)),
        longitude=slice(bounds[0], bounds[2]),
        latitude=slice(bounds[1], bounds[3]),
    )

    clipped_data = subset.rio.clip([shape(transposition_region.geometry)], drop=True, all_touched=True)
    transpose = Transpose(
        clipped_data[AORC_PRECIP_VARIABLE].sum(dim="time", skipna=True, min_count=1),
        shape(watershed.geometry),
        AORC_X_VAR,
        AORC_Y_VAR,
    )
    return transpose.valid_spaces_polygon

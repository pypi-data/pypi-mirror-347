from __future__ import annotations

import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Mapping, Sequence

import pandas as pd
import pystac
import pystac_client
import xarray as xr

from mccn.config import (
    CubeConfig,
    FilterConfig,
    ProcessConfig,
)
from mccn.drawer import Canvas, Rasteriser
from mccn.extent import GeoBoxBuilder
from mccn.loader.point import PointLoader
from mccn.loader.raster import RasterLoader
from mccn.loader.vector import VectorLoader
from mccn.parser import Parser

if TYPE_CHECKING:
    from odc.geo.geobox import GeoBox

    from mccn._types import (
        CRS_T,
        AnchorPos_T,
        BBox_T,
        DType_Map_T,
        Dtype_T,
        MergeMethod_Map_T,
        MergeMethod_T,
        Nodata_Map_T,
        Nodata_T,
        Resolution_T,
        Shape_T,
        TimeGroupby,
    )


class EndpointException(Exception): ...


class EndpointType(Exception): ...


class MCCN:
    def __init__(
        self,
        # Item discovery
        endpoint: str | Path | tuple[str, str] | None = None,
        collection: pystac.Collection | None = None,
        items: Sequence[pystac.Item] | None = None,
        # Geobox config
        shape: Shape_T | None = None,
        resolution: Resolution_T | None = None,
        bbox: BBox_T | None = None,
        anchor: AnchorPos_T = "default",
        crs: CRS_T = 4326,
        # Filter config
        geobox: GeoBox | None = None,
        start_ts: str | pd.Timestamp | datetime.datetime | None = None,
        end_ts: str | pd.Timestamp | datetime.datetime | None = None,
        bands: set[str] | None = None,
        mask_only: bool = False,
        use_all_vectors: bool = True,
        # Cube config
        x_dim: str = "x",
        y_dim: str = "y",
        t_dim: str = "time",
        mask_name: str = "__MASK__",
        combine_mask: bool = False,
        # Process config
        rename_bands: Mapping[str, str] | None = None,
        process_bands: Mapping[str, Callable] | None = None,
        nodata: Nodata_Map_T = 0,
        nodata_fallback: Nodata_T = 0,
        time_groupby: TimeGroupby = "time",
        merge_method: MergeMethod_Map_T = None,
        merge_method_fallback: MergeMethod_T = "replace",
        dtype: DType_Map_T = None,
        dtype_fallback: Dtype_T = "float64",
        # Multi-processing
        num_workers: int = 4,
    ) -> None:
        # Fetch Collection
        self.items = self.get_items(items, collection, endpoint)
        # Make geobox
        self.geobox = self.build_geobox(
            self.items, shape, resolution, bbox, anchor, crs, geobox
        )
        # Prepare configs
        self.filter_config = FilterConfig(
            geobox=self.geobox,
            start_ts=start_ts,
            end_ts=end_ts,
            bands=bands,
            mask_only=mask_only,
            use_all_vectors=use_all_vectors,
        )
        self.cube_config = CubeConfig(
            x_dim=x_dim,
            y_dim=y_dim,
            t_dim=t_dim,
            mask_name=mask_name,
            combine_mask=combine_mask,
        )
        self.process_config = ProcessConfig(
            rename_bands,
            process_bands,
            nodata,
            nodata_fallback,
            time_groupby,
            merge_method,
            merge_method_fallback,
            dtype,
            dtype_fallback,
        )
        # Parse items
        self.parser = Parser(self.filter_config, self.items)
        self.parser()
        # Prepare canvas
        self.canvas = Canvas.from_geobox(
            self.cube_config.x_dim,
            self.cube_config.y_dim,
            self.cube_config.t_dim,
            self.cube_config.spatial_ref_dim,
            self.geobox,
            self.process_config.dtype,
            self.process_config.dtype_fallback,
            self.process_config.nodata,
            self.process_config.nodata_fallback,
            self.process_config.merge_method,
            self.process_config.merge_method_fallback,
        )
        self.rasteriser = Rasteriser(canvas=self.canvas)
        self.point_loader: PointLoader = PointLoader(
            self.parser.point,
            self.rasteriser,
            self.filter_config,
            self.cube_config,
            self.process_config,
        )
        self.vector_loader = VectorLoader(
            self.parser.vector,
            self.rasteriser,
            self.filter_config,
            self.cube_config,
            self.process_config,
        )
        self.raster_loader: RasterLoader = RasterLoader(
            self.parser.raster,
            self.rasteriser,
            self.filter_config,
            self.cube_config,
            self.process_config,
        )
        self.num_workers = num_workers

    def load(self) -> xr.Dataset:
        self.raster_loader.load()
        self.vector_loader.load()
        self.point_loader.load()
        return self.rasteriser.compile()

    @staticmethod
    def build_geobox(
        items: list[pystac.Item],
        shape: Shape_T | None = None,
        resolution: Resolution_T | None = None,
        bbox: BBox_T | None = None,
        anchor: AnchorPos_T = "default",
        crs: CRS_T = 4326,
        # Filter config
        geobox: GeoBox | None = None,
    ) -> GeoBox:
        if geobox:
            return geobox
        try:
            builder = GeoBoxBuilder(crs, anchor=anchor)
            if bbox:
                builder = builder.set_bbox(bbox)
            if resolution is not None:
                if not isinstance(resolution, tuple):
                    resolution = (resolution, resolution)
                builder = builder.set_resolution(*resolution)
            if shape:
                if not isinstance(shape, tuple):
                    shape = (shape, shape)
                builder = builder.set_shape(*shape)
            return builder.build()
        except Exception:
            if not shape:
                raise ValueError(
                    "Unable to build geobox. For simplicity, user can pass a shape parameter, which will be used to build a geobox from collection."
                )
            return GeoBoxBuilder.from_items(items, shape, anchor)

    @staticmethod
    def get_geobox(
        collection: pystac.Collection,
        geobox: GeoBox | None = None,
        shape: int | tuple[int, int] | None = None,
    ) -> GeoBox:
        if geobox is not None:
            return geobox
        if shape is None:
            raise ValueError(
                "If geobox is not defined, shape must be provided to calculate geobox from collection"
            )
        return GeoBoxBuilder.from_collection(collection, shape)

    @staticmethod
    def get_items(
        items: Sequence[pystac.Item] | None = None,
        collection: pystac.Collection | None = None,
        endpoint: str | tuple[str, str] | Path | None = None,
    ) -> list[pystac.Item]:
        if items:
            return list(items)
        collection = MCCN.get_collection(endpoint, collection)
        return list(collection.get_items(recursive=True))

    @staticmethod
    def get_collection(
        endpoint: str | tuple[str, str] | Path | None,
        collection: pystac.Collection | None = None,
    ) -> pystac.Collection:
        """Try to load collection from endpoint.

        Raises `EndpointType` if endpoint is not an acceptable type, or `EndpointException` if
        endpoint is not reachable
        """
        if collection:
            return collection
        if not endpoint:
            raise ValueError("Either a collection or an endpoint must be provided")
        try:
            if isinstance(endpoint, tuple):
                href, collection_id = endpoint
                return pystac_client.Client.open(href).get_collection(collection_id)
            if isinstance(endpoint, Path | str):
                return pystac.Collection.from_file(str(endpoint))
            raise EndpointType(
                f"Expects endpoint as a local file path or a (api_endpoint, collection_id) tuple. Receives: {endpoint}"
            )
        except EndpointType as e:
            raise e
        except Exception as exception:
            raise EndpointException from exception

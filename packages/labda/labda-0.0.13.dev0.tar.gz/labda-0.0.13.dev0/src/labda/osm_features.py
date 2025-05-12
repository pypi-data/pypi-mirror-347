from pathlib import Path
from typing import Any, Self

import osmnx as ox
import pandas as pd
from pydantic import BaseModel
from pyproj import CRS
from shapely import wkb

from labda.spatial.utils import df_to_gdf

from .spatial.utils import change_crs, get_crs_info


class Features(BaseModel):
    df: pd.DataFrame
    crs: CRS | str | None = None
    buffer: float | None = None
    tags: dict[str, Any] | None = None

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_parquet(
        cls,
        path: Path | str,
    ) -> Self:
        if isinstance(path, str):
            path = Path(path)

        df = pd.read_parquet(path)
        metadata = df.attrs
        crs = metadata.get("crs")
        buffer = metadata.get("buffer")
        tags = metadata.get("tags")
        df["geometry"] = df["geometry"].apply(wkb.loads)

        return cls(df=df, crs=crs, buffer=buffer, tags=tags)  # type: ignore

    def to_parquet(self, path: str | Path) -> None:
        if isinstance(path, str):
            path = Path(path)

        path.parent.mkdir(
            parents=True, exist_ok=True
        )  # Create directory if it doesn't exist.

        metadata = self.model_dump(exclude={"df"})  # type: ignore

        if "geometry" in self.df.columns:
            df = pd.DataFrame(self.df)
            df.attrs = metadata  # type: ignore
            df["geometry"] = df["geometry"].apply(wkb.dumps)
            df.to_parquet(path)
        else:
            self.df.attrs = metadata  # type: ignore
            self.df.to_parquet(path)
            self.df.attrs = {}

        print(f"Parquet file saved to '{path}'.")

    def infer_crs(self, crs: str | CRS = "EPSG:4326") -> tuple[str, str]:
        return get_crs_info(self.df, crs=crs)  # type: ignore

    def set_crs(self, crs: str | CRS = "infer") -> None:
        source_crs = self.crs

        if not source_crs:
            raise ValueError(
                "Source CRS is missing. Please provide a valid CRS in the metadata."
            )

        if crs == "infer":
            crs, unit = self.infer_crs()

        self.df = change_crs(self.df, source_crs, crs)
        self.crs = crs
        print(f"CRS changed from {source_crs} to {self.crs}.")

    @classmethod
    def from_dataframe(
        cls,
        df: pd.DataFrame,
        crs: CRS | str,
        buffer: float = 100,
        tags: dict[str, Any] = {"building": True},
    ) -> Self:
        # NOTE: It works now oly on trips, in future it will work with STDBSCAN.
        df = df.loc[df["trip_status"].isin(["stationary", "pause"])]
        gdf = df_to_gdf(df, crs)

        boundaries = gdf.groupby("trip_id")["geometry"].apply(
            lambda x: x.union_all().convex_hull.buffer(buffer)
        )
        boundaries = boundaries.set_crs(crs).to_crs(epsg=4326).union_all()

        gdf = ox.features_from_polygon(boundaries, tags)  # type: ignore
        gdf.to_crs(crs, inplace=True)
        gdf.reset_index(level=0, inplace=True)
        gdf.index.name = "osm_id"
        gdf = gdf[gdf["element"] == "way"]
        gdf["features"] = "stationary"

        if gdf.empty:
            raise ValueError("No features found.")

        df = pd.DataFrame(gdf)

        return cls(df=df, crs=str(crs), buffer=buffer, tags=tags)  # type: ignore

from datetime import datetime, time
from typing import Annotated, Any, Literal, Self

import geopandas as gpd
import numpy as np
import osmnx as ox
import pandas as pd
from geopy.exc import GeocoderServiceError
from geopy.geocoders import Nominatim
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    model_validator,
)
from pyproj import CRS
from shapely.geometry import MultiPolygon, Polygon

from ..core.utils import filter_by_temporal_intervals
from .contexts import detect_spatial_context
from .utils import df_to_gdf, valid_coordinates

# TODO: Ideally deleted geopy library and use Nomatim directly (their package)

TEMPLATES = {
    "home": {
        "start": time(22, 0, 0),
        "end": time(6, 0, 0),
        "tags": {"building": True},
        "elements": ["way"],
        "days": [0, 1, 2, 3, 4],
    },
    "school": {
        "start": time(8, 0, 0),
        "end": time(14, 0, 0),
        "tags": {"amenity": "school"},
        "elements": ["way"],
        "days": None,
    },
}


def boundaries_from_dataframe(
    df: pd.DataFrame,
    crs: CRS | str,
    group_on: str | None = None,
    buffer: float = 100,
) -> MultiPolygon | Polygon:
    df = valid_coordinates(df)
    gdf = df_to_gdf(df, crs)

    if group_on is not None:
        polygon = (
            gdf.groupby(group_on)["geometry"]
            .apply(lambda x: x.union_all().convex_hull.buffer(buffer))
            .set_crs(crs)
            .to_crs(epsg=4326)
            .union_all()
        )
        polygon = MultiPolygon(polygon)
    else:
        polygon = gdf["geometry"].union_all().convex_hull.buffer(buffer)
        polygon = gpd.GeoSeries(polygon, index=[0], crs=crs).to_crs(epsg=4326).iloc[0]

    return polygon


def check_matching_crs(left: Any, right: Any) -> None:
    if isinstance(left, str):
        left = CRS.from_user_input(left)
    if isinstance(right, str):
        right = CRS.from_user_input(right)

    if left != right:
        raise ValueError("CRS mismatch: {left} != {right}")


def fix_nan(value: Any) -> Any:
    if isinstance(value, float):
        value = None if np.isnan(value) else value
    else:
        return value


def fix_building(value: Any) -> str | bool | None:
    return True if value == "yes" else value


def parse_leisure(value: Any) -> str | None:
    value = fix_nan(value)

    if value and value not in ["common"]:
        return value


class Location(BaseModel):
    name: str | None = None
    geometry: Polygon

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="ignore",
    )

    @staticmethod
    def get_polygon_intersection(left: Polygon, right: Polygon) -> dict[str, Any]:
        if isinstance(left, Polygon) and isinstance(right, Polygon):

            intersection_area = left.intersection(right).area
            intersected = True if intersection_area > 0 else False

            if intersected:
                union_area = left.union(right).area
                intersection_area_ratio = intersection_area / union_area
            else:
                intersection_area_ratio = 0

            return {
                "intersection": intersected,
                "ratio": intersection_area_ratio,
                "area": intersection_area,
            }

    @classmethod
    def from_context(cls, context: dict[str, Any]) -> Self:
        return cls(
            name=context.get("context"),
            geometry=context.get("geometry"),
        )


class LocationOSM(Location):
    osm_id: int
    wiki_id: Annotated[str | None, BeforeValidator(fix_nan)] = Field(
        default=None, alias="wikidata"
    )
    # address: Annotated[str | None, BeforeValidator(fix_nan)]
    type: Literal["node", "way", "relation"] = Field(alias="element")
    name: Annotated[str | None, BeforeValidator(fix_nan)] = None
    geometry: Polygon
    amenity: Annotated[str | None, BeforeValidator(fix_nan)] = None
    building: Annotated[
        str | bool | None, BeforeValidator(fix_nan), BeforeValidator(fix_building)
    ] = None
    tags: list[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def validate_tags(cls, values: Any) -> Any:
        tags = []

        tags.append(parse_leisure(values.get("leisure")))
        values["tags"] = [tag for tag in tags if tag is not None]

        return values

    def intersects(
        self, df: pd.DataFrame, crs: str, buffer: float = 10
    ) -> dict[str, Any]:
        geometry = self._get_geometry_in_crs(crs).buffer(buffer)
        result = detect_spatial_context(df, crs, geometry).value_counts()

        true = result.get(True, 0)
        false = result.get(False, 0)
        n_points = true + false
        probability = true / n_points

        return {
            "total": int(n_points),
            "intersects": int(true),
            "probability": float(probability),
        }

    def _get_geometry_in_crs(self, crs: str | CRS) -> Polygon:
        return gpd.GeoSeries([self.geometry], crs="EPSG:4326").to_crs(crs).iloc[0]

    def fetch_nominatim(self) -> None:
        centroid = self.geometry.centroid
        geolocator = Nominatim(user_agent=str(self.osm_id))

        time.sleep(1)  # To avoid hitting the rate limit

        try:
            result = geolocator.reverse(f"{centroid.y}, {centroid.x}").raw

            return {
                "address": result.get("address"),
                "type": result.get("type"),
            }
        except GeocoderServiceError as e:
            print(f"Error fetching data from Nominatim: {e}")
            return None


class Locations(BaseModel):
    values: list[Location | LocationOSM] = Field(default_factory=list)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra="ignore",
    )

    @classmethod
    def from_polygon(
        cls,
        polygon: Polygon | MultiPolygon,
        tags: dict[str, Any],
        elements: list[Literal["way", "node", "relation"]] | None = None,
        geometry: list[Literal["Point", "LineString", "Polygon"]] | None = None,
    ) -> Self:
        gdf = ox.features_from_polygon(polygon, tags)  # type: ignore

        if gdf.empty:
            raise ValueError("No features found.")

        gdf.reset_index(level=0, inplace=True)
        gdf.index.name = "osm_id"

        if elements is not None:
            gdf = gdf[gdf["element"].isin(elements)]

        if geometry is not None:
            gdf = gdf[gdf["geometry"].type.isin(geometry)]

        df = pd.DataFrame(gdf).reset_index().to_dict(orient="records")

        return cls(values=df)

    @classmethod
    def from_dataframe(
        cls,
        df: pd.DataFrame,
        crs: CRS | str,
        tags: dict[str, Any],
        buffer: float = 100,
        group_on: str | None = None,
        elements: list[Literal["way", "node", "relation"]] | None = None,
        geometry: list[Literal["Point", "LineString", "Polygon"]] | None = None,
    ) -> Self:
        multipolygon = boundaries_from_dataframe(df, crs, group_on, buffer)

        return cls.from_polygon(multipolygon, tags, elements, geometry)

    @property
    def df(self) -> pd.DataFrame:
        return pd.DataFrame.from_records(
            self.model_dump()["values"],
        )

    @property
    def gdf(self) -> gpd.GeoDataFrame:
        return df_to_gdf(
            self.df,
            crs="EPSG:4326",
            geometry="geometry",
        )

    def intersects(
        self,
        df: pd.DataFrame,
        crs: str | CRS,
    ) -> pd.DataFrame:
        results = []
        for location in self.values:
            result = location.intersects(df, crs)
            result["osm_id"] = location.osm_id
            results.append(result)

        results = (
            pd.DataFrame.from_records(results)
            .sort_values("probability", ascending=False)
            .reset_index(drop=True)
        )

        return results[["osm_id", "total", "intersects", "probability"]]

    def get_location(
        self,
        osm_id: int,
    ) -> LocationOSM:
        for location in self.values:
            if location.osm_id == osm_id:
                return location

        raise ValueError(f"Location with id {osm_id} not found.")

    @classmethod
    def find_location(
        cls,
        df: pd.DataFrame,
        crs: str | CRS,
        tags: dict[str, Any],
        elements: list[Literal["way", "node", "relation"]] | None = None,
        start: datetime | time | None = None,
        end: datetime | time | None = None,
        days: list[int] | None = None,
    ) -> tuple[Self, pd.DataFrame]:
        df = valid_coordinates(df)
        df = df[["latitude", "longitude"]]

        if start and end:
            df = filter_by_temporal_intervals(
                df,
                start,
                end,
            )

        if days:
            df = df[~df.index.weekday.isin(days)]

        locations = cls.from_dataframe(df, crs, tags, elements=elements)
        probabilities = locations.intersects(df, crs)

        probabilities = probabilities[probabilities["probability"] > 0]

        if probabilities.empty:
            raise ValueError("No location found for the given tags and time interval.")

        locations.values = [
            location
            for location in locations.values
            if location.osm_id in probabilities["osm_id"].values
        ]

        return locations, probabilities

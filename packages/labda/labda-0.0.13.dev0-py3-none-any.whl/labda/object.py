from copy import deepcopy
from pathlib import Path
from typing import Self

import pandas as pd
from pandera import DataFrameSchema
from pydantic import BaseModel, ConfigDict, Field
from shapely import wkb

from labda.metadata import Metadata


class BaseObject(BaseModel):
    id: str = Field(coerce_numbers_to_str=True)
    metadata: Metadata
    df: pd.DataFrame

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, metadata={self.metadata}, df[shape]={self.df.shape})"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_parquet(
        cls,
        path: Path | str,
    ) -> Self:
        """
        Creates an instance of LABDA data class from a Parquet file.
        Reads a Parquet file from the specified path, loads the data into a DataFrame and extracts metadata.

        Args:
            path (Path | str): The file path to the Parquet file.

        Returns:
            Self: An instance of the class initialized with data from the Parquet file.
        """

        if isinstance(path, str):
            path = Path(path)

        df = pd.read_parquet(path)

        if "geometry" in df.columns:
            df["geometry"] = df["geometry"].apply(wkb.loads)

        metadata = df.attrs
        metadata["id"] = path.stem
        df.attrs = {}

        return cls(id=metadata["id"], metadata=metadata, df=df)  # type: ignore

    def to_parquet(
        self,
        path: str | Path,
        overwrite: bool = False,
    ) -> None:
        """
        Save the DataFrame and metadata to Parquet format and writes it to the specified path.

        Args:
            path (str | Path): The file path where the Parquet file will be saved.
            overwrite (bool, optional): If True, overwrite the file if it exists. Defaults to False.

        Returns:
            None
        """

        if isinstance(path, str):
            path = Path(path)

        if not overwrite and path.exists():
            raise ValueError(
                f"File '{path}' already exists. Set overwrite to True to overwrite."
            )

        path.parent.mkdir(
            parents=True, exist_ok=True
        )  # Create directory if it doesn't exist.

        df = self.df.copy()

        if "geometry" in df.columns:
            df["geometry"] = df["geometry"].apply(wkb.dumps)

        df.attrs = self.metadata.model_dump()  # type: ignore
        df.to_parquet(path)
        del df

        print(f"Parquet file saved to '{path}'.")

    def validate(self, schema: DataFrameSchema) -> None:
        """
        Validates the DataFrame against the provided schema.

        Args:
            schema (DataFrameSchema): The schema to validate the DataFrame against.

        Raises:
            SchemaError: If the DataFrame does not conform to the schema.

        Side Effects:
            Modifies self.df in place by validating and reordering its columns to match the schema.
        """

        self.df = schema.validate(self.df)
        ordered_columns = [
            col for col in schema.columns.keys() if col in self.df.columns
        ]
        self.df = self.df[ordered_columns]

    def copy(self) -> Self:
        return deepcopy(self)

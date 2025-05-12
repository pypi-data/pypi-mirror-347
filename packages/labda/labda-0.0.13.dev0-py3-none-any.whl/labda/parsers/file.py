# from datetime import timedelta
# from pathlib import Path
# from zoneinfo import ZoneInfo

# import duckdb
# import pandas as pd

# # TODO: Not ready, should be checked.


# class FileIterator:
#     def __init__(
#         self,
#         path: Path,
#         size: timedelta = "1D",
#         overlap: timedelta = "15min",
#         timezone: ZoneInfo = "UTC",
#     ) -> None:
#         size = pd.Timedelta(size)
#         overlap = pd.Timedelta(overlap)

#         if isinstance(timezone, str):
#             timezone = ZoneInfo(timezone)

#         if isinstance(path, str):
#             path = Path(path)

#         self._index = 0
#         self.path = path
#         self.size = size
#         self.overlap = overlap
#         self.timezone = timezone
#         self.chunks = self._get_chunks(path, size, overlap)

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self._index < len(self.chunks):
#             chunk = self._load_chunk(self._index)

#             self._index += 1
#             return chunk

#         else:
#             raise StopIteration

#     def _get_chunks(
#         self,
#         path: Path,
#         size: pd.Timedelta,
#         overlap: pd.Timedelta,
#     ) -> pd.DataFrame:
#         connection = duckdb.connect()
#         connection.execute(f"SET TimeZone = '{self.timezone}'")
#         start, end = connection.execute(
#             f"SELECT min(datetime), max(datetime) FROM '{path}'"
#         ).fetchone()

#         chunks = pd.date_range(
#             start=start, end=end, freq=size, normalize=True
#         ).to_frame(index=False, name="start")
#         chunks.index.name = "chunk"
#         chunks["end"] = chunks["start"] + size
#         chunks.iat[0, 0] = start
#         chunks.iat[-1, -1] = end

#         chunks["start_overlap"] = chunks["start"] - overlap
#         chunks["end_overlap"] = chunks["end"] + overlap

#         return chunks

#     def _load_chunk(self, chunk: int) -> pd.DataFrame:
#         connection = duckdb.connect()
#         connection.execute(f"SET TimeZone = '{self.timezone}'")
#         chunk = self.chunks.iloc[chunk]
#         start, end = chunk["start"], chunk["end"]
#         start_overlap, end_overlap = chunk["start_overlap"], chunk["end_overlap"]

#         df = connection.execute(
#             f"SELECT * FROM '{self.path}' WHERE datetime >= '{start_overlap}' AND datetime < '{end_overlap}'"
#         ).fetchdf()

#         df["overlap"] = True
#         df.loc[(df.datetime >= start) & (df.datetime < end), "overlap"] = False
#         df.set_index("datetime", inplace=True)

#         return df

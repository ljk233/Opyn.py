
"""
A collection of functions that will return a Pandas `DataFrame`
representation of a dataset found in .data.
"""

from __future__ import annotations
import pandas as pd


class PandasLoader():
    """
    A helper class to read local csv files saved in a data directory
    not easily accessible by the cwd, and return it as a Pandas
    `DataFrame`.
    """

    def __init__(self, depth: int = 2, data_path: str = ".data") -> None:
        """
        Initialises the object.

        Args:
            depth: number of levels separating the cwd and the first \
                shared parent directory.
            data_path: path from the shared parent dir to the data dir.
        """
        self._depth: int = depth
        self._data_path: str = data_path

    @property
    def PATH(self) -> str:
        counter: int = 0
        rel_path: str = ''
        while counter < self._depth:
            rel_path = rel_path + '../'
            counter += 1
        return rel_path + self._data_path + '/'

    def get(self, f: str) -> pd.DataFrame:
        """
        Loads a csv file from the receiver's data directory and returns
        its a Pandas `DataFrame`.

        Args:
            f: file name

        Returns:
            a Pandas `DataFrame` representation of the csv file.
        """
        return pd.read_csv(self.PATH + f + '.csv')

    def list_files(self) -> list[str]:
        """
        Returns:
            a list of all current files in the data directory
        """
        from os import listdir
        return listdir(self.PATH)

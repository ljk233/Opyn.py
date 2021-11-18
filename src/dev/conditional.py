
"""
A module to help deal with conditional probablies.
"""

from __future__ import annotations
import pandas as pd
import numpy as np
from numpy.typing import ArrayLike


def a_given_b(df: pd.DataFrame, **kwargs) -> float:
    # calculates the probability P(A|B)
    cols: list[str] = []
    vals: list[str] = []
    for k, v in kwargs.items():
        cols.append(str(k))
        vals.append(str(v))
    # get nobs
    nobs = df.size / len(df.columns)
    anb: tuple[str, str] = vals[0], vals[1]
    b: str = vals[1]
    nobs_anb, nobs_b = 0, 0
    # collect tuple pairs of A,B
    pairs: list[str] = []
    for ndx in range(int(nobs)):
        pair: tuple[str] = str(df[cols[0]].iloc[ndx]), str(df[cols[1]].iloc[ndx])
        pairs.append(pair)
    for pair in pairs:
        if pair == anb:
            nobs_anb += 1
        if pair[1] == b:
            nobs_b += 1

    return nobs_anb / nobs_b


class Conditional:
    """
    A class to model the contingency tables.
    """

    def __init__(self, data: pd.DataFrame, A: str, B: str) -> None:
        self._data: pd.DataFrame = data
        self._colA: ArrayLike[str] = data[A].astype('str').to_numpy(dtype='str')
        self._colB: ArrayLike[str] = data[B].astype('str').to_numpy(dtype='str')

    @property
    def AB(self) -> list[tuple[str]]:
        # counts the number of obs of A and B
        

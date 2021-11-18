
"""
`opyn.stats.sampling`

TODO: Add module sting
"""


# %%
from __future__ import annotations
from . import dataclasses
from scipy import stats
from math import sqrt
from collections import namedtuple
import pandas as pd
from numpy.typing import ArrayLike


# %%
z: stats.rv_continuous = stats.norm
bern: stats.rv_discrete = stats.bernoulli


def to_namedtuple(
    res: tuple[float, float], is_type: str, prec: int = 4
) -> namedtuple[float, float]:
    """
    Used for results for `statsmodels` results, which returns just a
    tuple.

    Args:
        res: a tuple of floats
        is_type: must be one of `['confint', 'hypothtest']`
        prec: precision to return the results

    Returns:
        tuple from `statsmodels` as a `namedtuple`

    Raises:
        AssertionError: arg `is_type` not in `['confint', 'hypothtest']`
    """
    assert is_type in ['confint', 'hypothtest'], (
        f"{is_type} is not in {['confint', 'hypothtest']}")
    if is_type == 'confint':
        nt: namedtuple = namedtuple('zconfint', ['lower', 'upper'])
    else:  # is_type == 'hypothtest':
        nt: namedtuple = namedtuple('Result', ['zstat', 'pval'])

    return nt(round(res[0], prec), round(res[1], prec))


class ZSample():
    """Models a one or two sample **z**-test.

    Implemented to support scenarios where the sample mean, standard deviation,
    and number of observations from some population are given, rather the data.
    """

    def __init__(self, mean: float, std: float, nobs: int) -> None:
        """
        Args:
            mean: sample mean
            std: sample standard deviation
            nobs: sample size
        """
        self._mean: float = mean
        self._std: float = std
        self._nobs: int = nobs

    @property
    def ste_mean(self) -> float:
        """
        """
        return self._std / sqrt(self._nobs)

    @property
    def mean(self) -> float:
        """
        """
        return self._mean

    @property
    def std(self) -> float:
        """
        """
        return self._std

    @property
    def nobs(self) -> int:
        """
        """
        return self._nobs

    def zconfint_mean(
        self, a: float = 0.05, prec: int = 4
    ) -> dataclasses.ZConfInt:
        """
        Two-sided approximate confidence interval for the sample.

        Args:
            a: Significance level for the confidence interval
            prec: Precision of the returned boundaries

        Returns:
            datacass representation of the confidence interval
        """
        zval: float = z.ppf(1-a/2)
        res = self.mean - zval*self.ste_mean, self.mean + zval*self.ste_mean
        return dataclasses.ZConfInt(res[0], res[1])

    def twosided_ztest_mean(
        self, mu0: float = 0.0, prec: int = 4
    ) -> dataclasses.ZTest:
        """
        Returns the results of a two-sided **z**-test of the null
        hypothesis that the mean is equal to `mu0`.

        Args:
            mu0: hypothesized value for the mean
            prec: precision of the returned results

        Returns:
            dataclass representation of the results of the two-sided \
                **z**-test
        """
        zstat: float = (self.mean - mu0) / self.ste_mean
        if zstat <= 0:
            pval: float = z.cdf(x=zstat)
        else:
            pval: float = z.sf(x=zstat)
        res = zstat, 2*pval
        return dataclasses.ZTest(res[0], res[1])

    def onesided_ztest_mean(
        self, alternative: str, mu0: float = 0.0, prec: int = 4
    ) -> dataclasses.ZTest:
        """
        Returns the results of a one-sided **z**-test of the null
        hypothesis that the mean is equal to `mu0`.

        Args:
            alternative: alternative hypothesis, *H1*, has to be \
                one of the following: `['larger', 'smaller']`
            mu0: hypothesized value for the mean
            prec: precision of the returned results

        Returns:
            **zstat, pval**:
                z statistic and p-value

        Raises:
            AssertionError: `alternative` not in \
                `['larger', 'smaller']`
        """
        assert alternative in ['larger', 'smaller'], (
            f"{alternative} not one of [larger, smaller]"
        )
        zstat: float = (self.mean - mu0) / self.ste_mean
        if alternative == 'larger':
            pval: float = z.sf(x=zstat)
        else:
            pval: float = z.cdf(x=zstat)
        res = zstat, pval
        return dataclasses.ZTest(res[0], res[1])


# %%
class PairedSamples():
    """
    *class* `opyn.stats.sampling.PairedSamples`

    A simple class to model paired continuous random variables as
    and object.
    It is a simple implementation to calculate the covariance and
    Pearson's correlation coefficient.

    *Note, it is expected this class will be deprecated in the future.*
    """

    def __init__(self, x: ArrayLike[float], y: ArrayLike[float]) -> None:
        """
        Initialises the object.

        Args:
            x: first sample
            y: seond sample
        """
        self._x: ArrayLike[float] = x
        self._y: ArrayLike[float] = y

    @property
    def x(self) -> ArrayLike[float]:
        """
        """
        return self._x

    @property
    def y(self) -> ArrayLike[float]:
        """
        """
        return self._y

    @property
    def size(self) -> float:
        """
        """
        return self.x.size

    @property
    def cov(self) -> float:
        """
        """
        res_x: ArrayLike[float] = self.x - self.x.mean()
        res_y: ArrayLike[float] = self.y - self.y.mean()
        num: ArrayLike[float] = (res_x * res_y).sum()
        return num / (self.size - 1)

    @property
    def corr_coeff(self) -> float:
        """
        """
        return self.cov / (self.x.std() * self.y.std())

    def from_pandas(df: pd.DataFrame, cols: list[str]) -> PairedSamples:
        """
        Initialises and returns a new PairedSamples object from a
        **Pandas** `DataFrame`.
        It is expected that `cols` will contain exactly two `str`
        elements that both match column titles in df.

        A warning is printed if the column titles are the same.

        Args:
            df: a **Pandas** `DataFrame`
            cols: columns that are paired in arg `df`

        Raises:
            TypeError: if arg `df` is not a **Pandas** `DataFrame`
            AssertionError: if cols are not column titles in arg `df`
            AssertionError: if `len(cols)` is not equal to 2

        Returns:
            an initialised `PairedSamples` object
        """
        if not isinstance(df, pd.DataFrame):
            errstr = f"df is of type {type(df).__name__}, not pd.DataFrame"
            raise TypeError(errstr)
        for a_col in cols:
            assert a_col in df.columns, f"'{a_col}' is not a column in df"
        assert len(cols) == 2, f"cols {cols} is not a list of two str"
        if cols[0] == cols[1]:
            print("Warning: passed over the same column title twice")

        return PairedSamples(x=df[cols[0]], y=df[cols[1]])

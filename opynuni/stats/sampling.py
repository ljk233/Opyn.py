
"""
`opynuni.stats.sampling`

TODO: Add module sting
"""


# %%
from __future__ import annotations
from scipy import stats
from math import sqrt
from collections import namedtuple
import pandas as pd
import numpy as np
from numpy.typing import ArrayLike


# %%
z: stats.rv_continuous = stats.norm
bern: stats.rv_discrete = stats.bernoulli


def statsmodel_to_namedtuple(
    res: tuple[float, float], is_type: str, prec: int = 4
) -> namedtuple[float, float]:
    """
    Used for `statsmodels` results, which returns just a tuple.

    Args:
        res: a tuple of floats
        is_type: must be one of `['confint', 'hypothtest']`
        prec: precision to return the results

    Returns:
        tuple from `statsmodels` as a namedtuple

    Raises:
        AssertionError: arg `is_type` not in `['confint', 'hypothtest']`
    """
    assert is_type in ['confint', 'hypothtest'], (
        f"{is_type} is not in {['confint', 'hypothtest']}")
    if is_type == 'confint':
        nt: namedtuple = namedtuple('zconfint', ['lower', 'upper'])
    else:  # is_type == 'hypothtest':
        nt: namedtuple = namedtuple('Result', ['zstat', 'pval'])

    return nt(
        round(res[0], prec),
        round(res[1], prec)
    )


class ZSample():
    """
    *class* `opynuni.stats.sampling.ZSample`

    A class designed to model questions where we are given the sample
    mean, standard deviation, and number of observations from some
    population.
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
    ) -> namedtuple[float, float]:
        """
        Two-sided approximate confidence interval for the sample.

        Args:
            a: Significance level for the confidence interval
            prec: Precision of the returned boundaries

        Returns:
            Lower and upper boundaries of confidence interval
        """
        zval: float = z.ppf(1-a/2)
        res: namedtuple = namedtuple(
                                            'zconfint', ['lower', 'upper']
                                        )
        return res(
            round(self.mean - zval*self.ste_mean, prec),
            round(self.mean + zval*self.ste_mean, prec)
            )

    def twosided_ztest_mean(
        self, mu0: float = 0.0, prec: int = 4
    ) -> namedtuple[float, float]:
        """
        Returns the results of a two-sided **z**-test of the null
        hypothesis that the mean is equal to `mu0`.

        Args:
            mu0: hypothesized value for the mean
            prec: precision of the returned results

        Returns:
            **zstat, pval**:
                z statistic and p-value
        """
        zstat: float = (self.mean - mu0) / self.ste_mean
        if zstat <= 0:
            pval: float = z.cdf(x=zstat)
        else:
            pval: float = z.sf(x=zstat)
        res: namedtuple = namedtuple('Result', ['zstat', 'pval'])
        return res(round(zstat, prec), round(2*pval, prec))

    def onesided_ztest_mean(
        self, alternative: str, mu0: float = 0.0, prec: int = 4
    ) -> namedtuple[float, float]:
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
        zstat: float = (self.mean - mu0) / self.ste
        if alternative == 'larger':
            pval: float = z.sf(x=zstat)
        else:
            pval: float = z.cdf(x=zstat)
        res: namedtuple = namedtuple('Res', ['zstat', 'pval'])
        return res(round(zstat, prec), round(pval, prec))


# %%
class PairedSamples():
    """
    A simple class to model paired continuous random variables as
    and object.
    It is a simple implementation to calculate the covariance and
    Pearson's correlation coefficient.

    *Note, it is expected this class will be depreceated in the future.*
    """

    def __init__(self, x: ArrayLike, y: ArrayLike) -> None:
        """
        Initialises the object.

        Args:
            x: first sample
            y: seond sample
        """
        self._x: ArrayLike = x
        self._y: ArrayLike = y

    @property
    def x(self) -> ArrayLike:
        return self._x

    @property
    def y(self) -> ArrayLike:
        return self._y

    @property
    def x_bar(self) -> float:
        return self.x.mean()

    @property
    def y_bar(self) -> float:
        return self.y.mean()

    @property
    def size(self) -> float:
        return self.x.size

    @property
    def num(self) -> float:
        """
        Returns:
            sum of the product of the residuals
        """
        ndx: int = 0
        sum: float = 0
        while ndx < self.size:
            xres: float = self.x[ndx] - self.x_bar
            yres: float = self.y[ndx] - self.y_bar
            sum += (xres * yres)
            ndx += 1
        return sum

    @property
    def denom(self) -> int:
        return self.size-1

    @property
    def cov(self) -> float:
        return self.num / self.denom

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
            print(
                "Warning: did you mean to pass over the same column title twice?"
                )

        return PairedSamples(x=df[cols[0]], y=df[cols[1]])


# %%
test = pd.DataFrame(columns=["1", "2", "3"])

PairedSamples.from_pandas(test, ["1", "2"])

# %%

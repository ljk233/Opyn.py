
"""A collection of dataclasses to represent various descriptions of results.
"""

# %%
from __future__ import annotations
from dataclasses import dataclass
import pandas as pd


def _as_df(obj: object) -> pd.DataFrame:
    """Return a representation of the given object as a DataFrame.
    """
    variables = obj.__dict__
    df: pd.DataFrame = pd.DataFrame(
        data=[variables.values()],
        index=[type(obj).__name__],
        columns=variables.keys()
    )
    return df


class _PDDataClass:
    """A helper class that can represent a dataclass as a **Pandas**
    `DataFrame`.
    """

    def as_df(self) -> pd.DataFrame:
        """Return a representation of the given object as a DataFrame.
        """
        df: pd.DataFrame = pd.DataFrame(
            data=[self.__dict__.values()],
            index=[type(self).__name__],
            columns=self.__dict__.keys()
        )
        return df


@dataclass
class ChiSqTest(_PDDataClass):
    """A dataclass to model the results returned from a chi-sqared test of no
    association.

    Attributes:
        chisq (float): Value of the **chi-squared** test statistic.
        pval (float): **p**-value of the **chi-squared** test.
        df (int): Degrees of freedom.
    """

    chisq: float
    pval: float
    df: int


@dataclass
class ZConfInt(_PDDataClass):
    """A dataclass to model an approximate 100(1-**alpha**)% **z**-interval.

    Attributes:
        estimate (float): Point estimate
        ese: (float): Estimated standard error
        lcb (float): Lower boundary
        ucb (float): Upper boundary
    """
    estimate: float
    ese: float
    lcb: float
    ucb: float


@dataclass
class TConfInt(_PDDataClass):
    """A dataclass to model an approximate 100(1-**alpha**)% **t**-interval.

    Attributes:
        estimate (float): Point estimate
        ese: (float): Estimated standard error
        lcb (float): Lower boundary
        ucb (float): Upper boundary
    """
    estimate: float
    ese: float
    lcb: float
    ucb: float


@dataclass
class RelativeRisk(_PDDataClass):
    """Model the relative risk of an observational study.

    Attributes:
        estimate (float): Point estimate
        lcb (float): Lower boundary
        ucb (float): Upper boundary
    """

    estimate: float
    ese: float
    lcb: float
    ucb: float


@dataclass
class OddsRatio(_PDDataClass):
    """A dataclass to model the odds ratio of an observational study.

    Attributes:
        estimate (float): Point estimate
        ese (float): Estimated standard error
        lcb (float): Lower boundary
        ucb (float): Upper boundary
    """

    estimate: float
    ese: float
    lcb: float
    ucb: float


@dataclass
class ConditionalOdds:
    """A dataclass to model the conditional odds used in an observational study.

    Attributes:
        a_given_b (float)
        a_given_not_b (float)
    """

    a_given_b: float
    a_given_not_b: float

    def __str__(self) -> str:
        return f"a_b={self.a_given_b:.6f}, a_not_b={self.a_given_not_b:.6f}"

    def __repr__(self) -> str:
        return f"conditionalodds({self})"


@dataclass
class Normal:
    """A dataclass to model the description of a normal distribution.

    Attributes:
        mean (float): Mean of the distribtribution.
        var (float): Variance of the distribution.
    """

    mean: float
    var: float

    def __str__(self) -> str:
        return f"mean={self.mean:.6f}, var={self.var:.6f}"

    def __repr__(self) -> str:
        return f"normal({self})"


@dataclass
class ZTest(_PDDataClass):
    """A dataclass to model the results of a **z**-test.

    Attributes:
        zstat (float): Test statistic.
        pval (float): Significance probability.
    """
    zstat: float
    pval: float


@dataclass
class TTest(_PDDataClass):
    """A dataclass to model the results of a **z**-test.

    Attributes:
        tstat (float): Test statistic.
        pval (float): Significance probability.
        dof (int): Degrees of Freedom
    """
    tstat: float
    pval: float
    dof: int


@dataclass
class PairedVars:
    """A dataclass to model the relationship between paired continuous
    variables.

    Attributes:
        cov (float): Covariance of the two variables.
        r (float): Pearson correlation coefficient.
    """

    cov: float
    r: float


@dataclass
class PearsonR(_PDDataClass):
    """A dataclass to model the relationship the Pearson correlation
    coefficient between two continuous variables.

    Attributes:
        r (float): Pearson correlation coefficient.
        pval (float): P-value of test of null correlation.
    """

    r: float
    pval: float

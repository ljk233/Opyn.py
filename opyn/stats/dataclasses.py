
"""A collection of dataclasses to represent various descriptions of results.
"""

# %%
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class ChiSqTest():
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

    def __str__(self) -> str:
        return (
            f"chisq={self.chisq:.6f}, pval={self.pval:.6f}, df={self.df}"
        )

    def __repr__(self) -> str:
        return f"chisqtest({self})"


@dataclass
class ZConfInt:
    """A dataclass to model an approximate 100(1-**alpha**)% **z**-interval.

    Attributes:
        lower (float): Lower boundary
        upper (float): Upper boundary
    """

    lower: float
    upper: float

    def __str__(self) -> str:
        return f"lower={self.lower:.6f}, upper={self.upper:.6f}"

    def __repr__(self) -> str:
        return f"zconfint({self})"


@dataclass
class RelativeRisk:
    """Model the relative risk of an observational study.

    Attributes:
        lower (float): Lower boundary
        point (float): Point estimate
        upper (float): Upper boundary
    """

    point: float
    lower: float
    upper: float

    def __str__(self) -> str:
        return(
            f"{self.point:.6f}"
            f", zconfint(lower={self.lower:.6f}, upper={self.upper:.6f})"
        )

    def __repr__(self) -> str:
        return f"relativerisk({self})"


@dataclass
class OddsRatio:
    """A dataclass to model the odds ratio of an observational study.

    Attributes:
        lower (float): Lower boundary
        point (float): Point estimate
        upper (float): Upper boundary
    """

    point: float = 0.0
    lower: float = 0.0
    upper: float = 0.0

    def __str__(self) -> str:
        return(
            f"point={self.point:.6f}"
            f", zconfint={{lower={self.lower:.6f}, upper={self.upper:.6f}}}"
        )

    def __repr__(self) -> str:
        return f"oddsratio({self})"


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
        return(
            f"a_b={self.a_given_b:.6f}, a_not_b={self.a_given_not_b:.6f}"
        )

    def __repr__(self) -> str:
        return f"conditonalodds({self})"


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
        return(
            f"mean={self.mean:.6f}"
            f", var={self.var:.6f}"
        )

    def __repr__(self) -> str:
        return f"normal({self})"


@dataclass
class ZTest:
    """A dataclass to model the results of a **z**-test.

    Attributes:
        zstat (float): Value of the **z**-statistic.
        pval (float): **p**-value of **z**-test.
    """

    zstat: float
    pval: float

    def __str__(self) -> str:
        return(
            f"zstat={self.zstat:.6f}"
            f", pval={self.pval:.6f}"
        )

    def __repr__(self) -> str:
        return f"ztest({self})"


@dataclass
class PairedVars:
    """A dataclass to model the relationship between paired continuous
    variables.

    Attributes:
        cov (float): Covariance of the two variables.
        r (float): Value of the Pearson correlation coefficient.
    """

    cov: float
    r: float

    def __str__(self) -> str:
        return(
            f"cov={self.cov:.6f}"
            f", r={self.r:.6f}"
        )

    def __repr__(self) -> str:
        return f"pairedvars({self})"


"""A collection of dataclasses to represent various descriptions of results.
"""

# %%
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class ChiSqTest():
    """Models the results of a chi-sqared test of no association.
    """

    _chisq: float = 0.0
    _pval: float = 0.0
    _df: int = 0

    @property
    def chisq(self) -> float:
        """
        """
        return float(self._chisq)

    @property
    def pval(self) -> float:
        """
        """
        return float(self._pval)

    @property
    def df(self) -> int:
        """
        """
        return self._df

    def __str__(self) -> str:
        """Return a string representation of the object.
        """
        return(
            f"chisq={self.chisq:.6f}, pval={self.pval:.6f}, df={self.df}"
        )

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Same as the `str` representation, but includes the class name.
        """
        return(
            f"ChiSqTest({self})"
        )


@dataclass
class ZConfInt:
    """Models an approximate **z**-interval.
    """

    _lower: float = 0.0
    _upper: float = 0.0

    @property
    def lower(self) -> float:
        """
        """
        return float(self._lower)

    @property
    def upper(self) -> float:
        """
        """
        return float(self._upper)

    def __str__(self) -> str:
        """Return a string representation of the object.
        """
        return(
            f"lower={self.lower:.6f}, upper={self.upper:.6f}"
        )

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Same as the `str` representation, but includes the class name.
        """
        return(
            f"zconfint({self})"
        )


@dataclass
class RelativeRisk:
    """A dataclass to model the relative risk of a cohort study.
    """

    _point: float = 0.0
    _lower: float = 0.0
    _upper: float = 0.0

    @property
    def point(self) -> float:
        return float(self._point)

    @property
    def lower(self) -> float:
        """
        """
        return float(self._lower)

    @property
    def upper(self) -> float:
        """
        """
        return float(self._upper)

    def __str__(self) -> str:
        """Return a string representation of the object.
        """
        return(
            f"point={self.point:.6f}"
            f", zconfint={{lower={self.lower:.6f}, upper={self.upper:.6f}}}"
        )

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Same as the `str` representation, but includes the class name.
        """
        return(
            f"RelativeRisk({self})"
        )


@dataclass
class OddsRatio:
    """A dataclass to model the odds ratio of a cohort and case-control study.
    """

    _point: float = 0.0
    _lower: float = 0.0
    _upper: float = 0.0

    @property
    def point(self) -> float:
        return float(self._point)

    @property
    def lower(self) -> float:
        """
        """
        return float(self._lower)

    @property
    def upper(self) -> float:
        """
        """
        return float(self._upper)

    def __str__(self) -> str:
        """Return a string representation of the object.
        """
        return(
            f"point={self.point:.6f}"
            f", zconfint={{lower={self.lower:.6f}, upper={self.upper:.6f}}}"
        )

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Same as the `str` representation, but includes the class name.
        """
        return(
            f"OddsRatio({self})"
        )


@dataclass
class ConditionalOdds:
    """Models the odds of disease given exposure in a cohort and case-control
    study.
    """

    _a_given_b: float = 0.0
    _a_given_not_b: float = 0.0

    @property
    def disease_exposed(self) -> float:
        """
        """
        return float(self._a_given_b)

    @property
    def disease_not_exposed(self) -> float:
        """
        """
        return float(self._a_given_not_b)

    @property
    def exposed_disease(self) -> float:
        """
        """
        return float(self._a_given_b)

    @property
    def exposed_no_disease(self) -> float:
        """
        """
        return float(self._a_given_not_b)

    def __str__(self) -> str:
        """Return a string representation of the object.
        """
        return(
            f"OD(A|B)={self.disease_exposed:.6f}"
            f", OD(A|NotB)={self.disease_not_exposed:.6f}"
        )

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Same as the `str` representation, but includes the class name.
        """
        return(
            f"ConditionalOdds({self})"
        )


@dataclass
class Normal:
    """Models a normal distribution.
    """

    _mean: float
    _var: float

    @property
    def mean(self) -> float:
        """
        """
        return float(self._mean)

    @property
    def var(self) -> float:
        """
        """
        return float(self._var)

    def __str__(self) -> str:
        """Return a string representation of the object.
        """
        return(
            f"mean={self.mean:.6f}"
            f", var={self.var:.6f}"
        )

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Same as the `str` representation, but includes the class name.
        """
        return(
            f"Normal({self})"
        )


@dataclass
class ZTest:
    """Models the results of a z-test.
    """

    _zstat: float
    _pval: float

    @property
    def zstat(self) -> float:
        """
        """
        return self._zstat

    @property
    def pval(self) -> float:
        """
        """
        return self._pval

    def __str__(self) -> str:
        """Return a string representation of the object.
        """
        return(
            f"zstat={self.zstat:.6f}"
            f", pval={self.pval:.6f}"
        )

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Same as the `str` representation, but includes the class name.
        """
        return(
            f"ztest({self})"
        )


@dataclass
class PairedVars:
    """Models the relationship between paired continuous variables.
    """

    _cov: float
    _r: float

    @property
    def cov(self) -> float:
        """
        """
        return self._cov

    @property
    def r(self) -> float:
        """
        """
        return self._corr_coeff

    def __str__(self) -> str:
        """Return a string representation of the object.
        """
        return(
            f"cov={self.cov:.6f}"
            f", r={self.r:.6f}"
        )

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Same as the `str` representation, but includes the class name.
        """
        return(
            f"pairedvars({self})"
        )

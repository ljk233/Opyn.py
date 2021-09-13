
"""A module to help perform analyses on cohort and case-control studies.
"""


from __future__ import annotations
from scipy import stats
from statsmodels.stats import contingency_tables
from . import adt
import pandas as pd
import numpy as np
from numpy.typing import ArrayLike
from typing import Union


class ContingencyTable:
    """A composite class to model a cohort or case-control study, as outlined
       by **M249.**
    """

    def __init__(self, obs: ArrayLike) -> None:
        """Initialises the object.

        Args:
            obs: some data structure representing the data.\
                Do not include any marginal totals.
        """
        self._obs: np.ndarray = np.array(obs)
        self._table2x2: contingency_tables.Table2x2 = (
            contingency_tables.Table2x2(self._obs)
        )
        self._row_labels: list[str] = ["Exposed", "Not Exposed"]
        self._col_labels: list[str] = ["Disease", "No Disease"]

    @property
    def row_labels(self) -> list[str]:
        """Return the object's row labels that will be included in a DataFrame.
        """
        return self._row_labels

    @row_labels.setter
    def row_labels(self, labels: list[str]) -> None:
        """Set the object's row labels that will be included in a DataFrame.
        """
        self._row_labels = labels

    @property
    def col_labels(self) -> list[str]:
        """Return the object's column labels that will be included in a
        DataFrame.
        """
        return self._col_labels

    @col_labels.setter
    def col_labels(self, labels: list[str]) -> None:
        """Set the object's column labels that will be included in a
        DataFrame.
        """
        self._col_labels = labels

    @property
    def table2x2(self) -> contingency_tables.Table2x2:
        """Return the receiver's instance of type `Table2x2`.
        """
        return self._table2x2

    def relative_risk(self, alpha: float = 0.05) -> adt.RelativeRisk:
        """Return the point and (1-alpha)% confidence interval for the relative
        risk.

        Args:
            alpha: Significance level for the confidence interval.

        Returns:
            Initialised object of type `RelativeRisk`.
        """
        res = self.table2x2.riskratio_confint(alpha)
        return adt.RelativeRisk(self.table2x2.riskratio, res[0], res[1])

    def odds_ratio(self, alpha: float = 0.05) -> adt.OddsRatio:
        """Return the point and (1-alpha)% confidence interval for the odds
        ratio.

        Args:
            alpha: Significance level for the confidence interval.

        Returns:
            Initialised object of type `OddsRatio`.
        """
        res = self.table2x2.oddsratio_confint(alpha)
        return adt.OddsRatio(self.table2x2.oddsratio, res[0], res[1])

    def conditional_odds(self) -> adt.OddsDiseaseExposure:
        """Returns the odds of disease given exposure, and disease given no
        exposure.

        Returns:
            Initialised instance of `OddsDiseaseExposure`.
        """
        # elements in the table
        a = self._obs[0][0]
        b = self._obs[0][1]
        c = self._obs[1][0]
        d = self._obs[1][1]
        # calculate odds
        de: float = a / b
        dne: float = c / d

        return adt.OddsDiseaseExposure(de, dne)

    def expected_freq(
        self, incl_row_totals: bool = False, incl_col_totals: bool = False
    ) -> pd.DataFrame:
        """Return the expected frequencies from a contingency table.

        Args:
            incl_row_totals: If True, then include the row marginal totals in\
                the DataFrame. Otherwise, do not include them.
            incl_col_totals: If True, then include the column marginal totals\
                in the the DataFrame. Otherwise, do not include them.

        Returns:
            A **Pandas** `DataFrame` representation of the expected\
                frequencies.
        """
        res = stats.contingency.expected_freq(self._obs)
        return (
            nparray_to_pandas(
                res,
                self,
                include_row_totals=incl_row_totals,
                include_col_totals=incl_col_totals)
        )

    def chi2_contribs(self) -> pd.DataFrame:
        """Return the chi-squared contributions for each observation used in a
        chi-squared test of no association.

        Returns:
            A **Pandas** `DataFrame` representation of the each observations\
                chi-squared contribution.
        """
        res = self.table2x2.chi2_contribs
        return (
            nparray_to_pandas(
                res,
                self,
                include_row_totals=False,
                include_col_totals=False
            )
        )

    def chi2_test(self) -> adt.ChiSqTest:
        """Return the results of a chi-squared test of no association.

        Returns:
            An initialised dataclass object of type `ChiSqTest`.
        """
        res = stats.chi2_contingency(self._obs, correction=False)
        return adt.ChiSqTest(res[0], res[1], res[2])

    def show_table(
        self, incl_row_totals: bool = False, incl_col_totals: bool = False
    ) -> pd.DataFrame:
        """Return the object observations as a DataFrame.

        Args:
            incl_row_totals: If True, then include the row marginal totals in\
                the DataFrame. Otherwise, do not include them.
            incl_col_totals: If True, then include the column marginal totals\
                in the the DataFrame. Otherwise, do not include them.

        Returns:
            Add desc
        """
        return (
            nparray_to_pandas(
                self._obs,
                self,
                include_row_totals=incl_row_totals,
                include_col_totals=incl_col_totals)
        )


class MultipleExposures:
    """
    """

    def __init__(
        self, exposure1: list[int], exposure2: list[int], reference: list[int]
    ) -> None:
        self.table1: ContingencyTable = (
            ContingencyTable([exposure1, reference]))
        self.table2: ContingencyTable = (
            ContingencyTable([exposure2, reference]))
        self._obs: np.ndarray = (
            np.array([exposure1, exposure2, reference]))

        self._exposure1_label: str = "First Exposure"
        self._exposure2_label: str = "Second Exposure"
        self._referece_label: str = "Reference Exposure"
        self._col_labels: list[str] = ["Disease", "No Disease"]
        self._update_labels_in_tables()

    def _update_labels_in_tables(self) -> None:
        self.table1.row_labels = [self.exposure1_label, self.reference_label]
        self.table2.row_labels = [self.exposure2_label, self.reference_label]
        self.table1.col_labels = self.col_labels
        self.table2.col_labels = self.col_labels

    @property
    def exposure1_label(self) -> str:
        return self._exposure1_label

    @exposure1_label.setter
    def exposure1_label(self, label: str) -> None:
        self._exposure1_label = label
        self._update_labels_in_tables()

    @property
    def exposure2_label(self) -> str:
        return self._exposure2_label

    @exposure2_label.setter
    def exposure2_label(self, label: str) -> None:
        self._exposure2_label = label
        self._update_labels_in_tables()

    @property
    def reference_label(self) -> str:
        return self._referece_label

    @reference_label.setter
    def reference_label(self, label: str) -> None:
        self._referece_label = label
        self._update_labels_in_tables()

    @property
    def col_labels(self) -> list[str]:
        return self._col_labels

    @col_labels.setter
    def col_labels(self, labels: list[str]) -> None:
        self._col_labels = labels
        self._update_labels_in_tables()

    @property
    def row_labels(self) -> list[str]:
        return (
            [self.exposure1_label,
             self.exposure2_label,
             self.reference_label])

    def expected_freq(
        self, incl_row_totals: bool = False, incl_col_totals: bool = False
    ) -> pd.DataFrame:
        """Return the expected frequencies from a contingency table.

        Args:
            incl_row_totals: If True, then include the row marginal totals in\
                the DataFrame. Otherwise, do not include them.
            incl_col_totals: If True, then include the column marginal totals\
                in the the DataFrame. Otherwise, do not include them.

        Returns:
            A **Pandas** `DataFrame` representation of the expected\
                frequencies.
        """
        res = stats.contingency.expected_freq(self._obs)
        return (
            nparray_to_pandas(
                res,
                self,
                include_row_totals=incl_row_totals,
                include_col_totals=incl_col_totals)
        )

    def chi2_contribs(self) -> pd.DataFrame:
        """Return the chi-squared contributions for each observation used in a
        chi-squared test of no association.

        Returns:
            A **Pandas** `DataFrame` representation of the each observations\
                chi-squared contribution.
        """
        exp: np.ndarray = stats.contingency.expected_freq(self._obs)
        res: np.ndarray = np.square(self._obs - exp) / exp
        return (
            nparray_to_pandas(
                res,
                self,
                include_row_totals=False,
                include_col_totals=False
            )
        )

    def chi2_test(self) -> adt.ChiSqTest:
        """Return the results of a chi-squared test of no association.

        Returns:
            An initialised dataclass object of type `ChiSqTest`.
        """
        res = stats.chi2_contingency(self._obs, correction=False)
        return adt.ChiSqTest(res[0], res[1], res[2])

    def show_table(
        self, incl_row_totals: bool = False, incl_col_totals: bool = False
    ) -> pd.DataFrame:
        """Return the object observations as a DataFrame.

        Args:
            incl_row_totals: If True, then include the row marginal totals in\
                the DataFrame. Otherwise, do not include them.
            incl_col_totals: If True, then include the column marginal totals\
                in the the DataFrame. Otherwise, do not include them.

        Returns:
            Add desc
        """
        return (
            nparray_to_pandas(
                self._obs,
                self,
                include_row_totals=incl_row_totals,
                include_col_totals=incl_col_totals)
        )


def nparray_to_pandas(
    array: np.ndarray, obj: Union(ContingencyTable, MultipleExposures),
    include_row_totals: bool = False, include_col_totals: bool = True
) -> pd.DataFrame:
    """
    Return a **numpy** array as a **pandas** DataFrame.

    Args:
        array: [description]
        obj: [description]

    Returns:
        [description]
    """

    # initialise a new DataFrame
    df: pd.DataFrame = pd.DataFrame(
        array, obj.row_labels, obj.col_labels)

    # melt the df, then pivot it
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Exposed Category"}, inplace=True)
    df = df.melt(id_vars="Exposed Category")
    df = df.pivot_table(
        index="Exposed Category",
        columns="variable",
        values="value",
        aggfunc=np.sum,
        margins=True,
        margins_name="Total")
    df.rename_axis(["Disease Category"], axis=1, inplace=True)

    # add the marginal totals if needed
    if not include_row_totals:
        df.drop(columns="Total", inplace=True)
    if not include_col_totals:
        df.drop(index="Total", inplace=True)

    return df

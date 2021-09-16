
"""A module to help perform analyses on various observatioanl studies.

This module was implemented following studies of M249, Book 1.
Currently only case-control studies and cohort studies are supported.

Classes:
    - **ExposureControl**:
        Models an observational study with two exposures.
    - **ThreeExposures**:
        Models an observational study with three exposure cateogries.

Dependencies:
    - **scipy**
    - **statsmodels**
    - **pandas**
    - **numpy**

Examples:
    - To be added.
"""


from __future__ import annotations
from scipy import stats
from statsmodels.stats import contingency_tables
from . import dataclasses
import pandas as pd
import numpy as np
from numpy.typing import ArrayLike
from typing import Union


class ExposureControl:
    """Models an observational study with two exposures.

    It has a composite relationship with `Table2x2` class from
    `statsmodels`, such that an `ExposureControl` *has-a* `Table2x2`.

    Parameters:
        obs (ArrayLike): Observations from the study. It is expected that\
            the data structure can be cast to a **numpy** `ndarray`.\
            See **[https://bit.ly/3kdQ7zg](statsmodels)** for examples.

    Attributes:
        col_labels (list[str]): Column labels to be used in a `DataFrame`.\
            Default is `["Disease", "No Disease"]`.
        obs (np.ndarray): Results of the study.
        row_labels (list[str]): Column labels to be used in a `DataFrame`.\
            Default is `["Exposed", "Not Exposed"]`.
        table2x2 (Table2x2): Initialised instance of **statsmodels**\
            `Table2x2` used for modelling the analysis.

    Warning:
        There is no type checking on **col_labels** and **row_label**.

    Methods:
        - **conditional odds**
            - Returns the conditonal odds associated with a study.
        - **expected_freq**
            - Return the expected frequencies from a contingency table under
            the hypothesis of no association.
        - **chi2_contribs**
            - Return the chi-squared contributions for each observation used
            in a chi-squared test of no association.
        - **chi2_test**
            - Return the results of a chi-squared test of no association.
        - **odds_ratio**
            - Return the point and (1-alpha)% confidence interval estimates
            for the odds ratio.
        - **relative_risk**
            - Return the point and (1-alpha)% confidence interval estimates
            for the relative risk.
        - **show_table**
            - Return a contingency table of the study.
    """

    def __init__(self, obs: ArrayLike) -> None:
        """Initialises the object.

        Args:
            obs: some data structure representing the data.\
                Do not include marginal totals.\
                Example data structure: `[[1, 5], [10, 15]]`
        """
        self.obs: np.ndarray = np.array(obs)
        self.table2x2: contingency_tables.Table2x2 = (
            contingency_tables.Table2x2(self.obs)
        )
        self.row_labels: list[str] = ["Exposed", "Not Exposed"]
        self.col_labels: list[str] = ["Disease", "No Disease"]

    def relative_risk(
        self, alpha: float = 0.05
    ) -> dataclasses.RelativeRisk:
        """Return the point and (1-alpha)% confidence interval estimates for
        the relative risk.

        Args:
            alpha: Significance level for the confidence interval.

        Returns:
            Point and (1-alpha)% confidence interval estimates for\
            the relative risk.
        """
        res = self.table2x2.riskratio_confint(alpha)
        return (
            dataclasses.RelativeRisk(self.table2x2.riskratio, res[0], res[1]))

    def odds_ratio(self, alpha: float = 0.05) -> dataclasses.OddsRatio:
        """Return the point and (1-alpha)% confidence interval estimates for
        the odds ratio.

        Args:
            alpha: Significance level for the confidence interval.

        Returns:
            Point and (1-alpha)% confidence interval estimates for\
            the odds ratio.
        """
        res = self.table2x2.oddsratio_confint(alpha)
        return dataclasses.OddsRatio(self.table2x2.oddsratio, res[0], res[1])

    def conditional_odds(self, is_cohort: bool) -> dataclasses.ConditionalOdds:
        """Returns the conditonal odds associated with a study.

        Args:
            is_cohort: If `True`, estimate disease given exposure.\
                Otherwise, estimate exposure given disease.**

        Returns:
            Conditonal odds associated with a study, either **OD(D|E),**\
                **OD(D|Not E)** or **OD(E|D), OD(E|Not D).**
        """
        # elements in the table
        a = self.obs[0][0]
        b = self.obs[0][1]
        c = self.obs[1][0]
        d = self.obs[1][1]

        if is_cohort:
            ab: float = a / b
            anb: float = c / d
        else:
            ab: float = a / c
            anb: float = b / d

        return dataclasses.ConditionalOdds(ab, anb)

    def expected_freq(
        self, incl_row_totals: bool = False, incl_col_totals: bool = False
    ) -> pd.DataFrame:
        """Return the expected frequencies from a contingency table under
        the hypothesis of no association.

        Args:
            incl_row_totals: If `True`, then include the row marginal\
                totals in the `DataFrame`. Otherwise, do not include them.
            incl_col_totals: If `True`, then include the column\
                marginal totals in the the `DataFrame`. Otherwise, do not\
                include them.

        Returns:
            Expected frequencies.
        """
        res = stats.contingency.expected_freq(self.obs)
        return (
            _nparray_to_pandas(
                res,
                self,
                include_row_totals=incl_row_totals,
                include_col_totals=incl_col_totals)
        )

    def chi2_contribs(self) -> pd.DataFrame:
        """Return the chi-squared contributions for each observation used in a
        chi-squared test of no association.

        Returns:
            chi-squared contributions.
        """
        res = self.table2x2.chi2_contribs
        return (
            _nparray_to_pandas(
                res,
                self,
                include_row_totals=False,
                include_col_totals=False
            )
        )

    def chi2_test(self) -> dataclasses.ChiSqTest:
        """Return the results of a chi-squared test of no association.

        Returns:
            Results of a chi-squared test of no association.
        """
        res = stats.chi2_contingency(self.obs, correction=False)
        return dataclasses.ChiSqTest(res[0], res[1], res[2])

    def show_table(
        self, incl_row_totals: bool = False, incl_col_totals: bool = False
    ) -> pd.DataFrame:
        """Return a contingency table of the study.

        Args:
            incl_row_totals: If `True`, then include the row marginal\
                totals in the `DataFrame`. Otherwise, do not include them.
            incl_col_totals: If `True`, then include the column marginal\
                totals in the the `DataFrame`. Otherwise, do not include them.

        Returns:
            Contingency table of the study.
        """
        return (
            _nparray_to_pandas(
                self.obs,
                self,
                include_row_totals=incl_row_totals,
                include_col_totals=incl_col_totals)
        )


class ThreeExposures:
    """Models an observational study where there are three exposures.

    It has a composite relationship with `statsmodels` `Table2x2` class,
    where an `ThreeExposures` *has-a* `ExposureControl`.
    """

    def __init__(
        self, exposure1: list[int], exposure2: list[int], reference: list[int]
    ) -> None:
        self.table1: ExposureControl = (
            ExposureControl([exposure1, reference]))
        self.table2: ExposureControl = (
            ExposureControl([exposure2, reference]))
        self.obs: np.ndarray = (
            np.array([exposure1, exposure2, reference]))

        self.exposure1_label: str = "First Exposure"
        self.exposure2_label: str = "Second Exposure"
        self.referece_label: str = "Reference Exposure"
        self.col_labels: list[str] = ["Disease", "No Disease"]
        self._update_labels_in_tables()

    def _update_labels_in_tables(self) -> None:
        self.table1.row_labels = [self.exposure1_label, self.reference_label]
        self.table2.row_labels = [self.exposure2_label, self.reference_label]
        self.table1.col_labels = self.col_labels
        self.table2.col_labels = self.col_labels

    @property
    def row_labels(self) -> list[str]:
        """Return the row labels.
        """
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
        res = stats.contingency.expected_freq(self.obs)
        return (
            _nparray_to_pandas(
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
        exp: np.ndarray = stats.contingency.expected_freq(self.obs)
        res: np.ndarray = np.square(self.obs - exp) / exp
        return (
            _nparray_to_pandas(
                res,
                self,
                include_row_totals=False,
                include_col_totals=False
            )
        )

    def chi2_test(self) -> dataclasses.ChiSqTest:
        """Return the results of a chi-squared test of no association.

        Returns:
            An initialised dataclass object of type `ChiSqTest`.
        """
        res = stats.chi2_contingency(self.obs, correction=False)
        return dataclasses.ChiSqTest(res[0], res[1], res[2])

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
            _nparray_to_pandas(
                self.obs,
                self,
                include_row_totals=incl_row_totals,
                include_col_totals=incl_col_totals)
        )


def _nparray_to_pandas(
    array: np.ndarray, obj: Union(ExposureControl, ThreeExposures),
    include_row_totals: bool = False, include_col_totals: bool = True
) -> pd.DataFrame:
    """Helper function.
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

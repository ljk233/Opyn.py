

class ThreeExposures:
    """Models an observational study where there are three exposures.

    It has a composite relationship with `statsmodels` `Table2x2` class,
    where an `ThreeExposures` *has-a* `TwoByTwo`.
    """

    def __init__(
        self, exposure1: list[int], exposure2: list[int], reference: list[int]
    ) -> None:
        self.table1: TwoByTwo = (
            TwoByTwo([exposure1, reference]))
        self.table2: TwoByTwo = (
            TwoByTwo([exposure2, reference]))
        self.obs: np.ndarray = (
            np.array([exposure1, exposure2, reference]))

        self.exposure1_label: str = "First Exposure"
        self.exposure2_label: str = "Second Exposure"
        self.reference_label: str = "Reference Exposure"
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


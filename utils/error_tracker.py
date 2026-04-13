class ErrorTracker:

    def detect_invalid_amount(self, df):
        """
        Detect non-numeric values in amount column
        """

        for index, value in enumerate(df["amount"]):

            try:
                float(value)

            except ValueError:
                raise ValueError(
                    f"Invalid amount at row {index + 1}, column 'amount'"
                )

        return True
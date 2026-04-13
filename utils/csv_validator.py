class CSVValidator:

    REQUIRED_COLUMNS = [
        "date",
        "description",
        "amount",
        "type"
    ]

    def validate_columns(self, df):
        """
        Check if required columns exist in dataframe
        """

        missing_columns = []

        for column in self.REQUIRED_COLUMNS:
            if column not in df.columns:
                missing_columns.append(column)

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        return True
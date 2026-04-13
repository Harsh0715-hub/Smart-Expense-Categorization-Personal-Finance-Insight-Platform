import streamlit as st
import pandas as pd
import io

class DataValidator:
    """
    Comprehensive data validation for transaction CSV files
    """
    
    REQUIRED_COLUMNS = ["date", "description", "amount", "type"]
    VALID_TYPES = ["credit", "debit"]
    
    def __init__(self):
        self.validation_results = {
            "errors": [],
            "warnings": [],
            "info": [],
            "valid": True
        }
    
    def validate_columns(self, df):
        """Check if all required columns exist"""
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            self.validation_results["errors"].append(
                f"❌ Missing required columns: {', '.join(missing_cols)}"
            )
            self.validation_results["valid"] = False
            return False
        self.validation_results["info"].append(
            f"✅ All required columns present: {', '.join(self.REQUIRED_COLUMNS)}"
        )
        return True
    
    def validate_column_types(self, df):
        """Validate data types in columns"""
        try:
            # Check if date column can be converted to datetime
            pd.to_datetime(df["date"], errors="coerce")
            date_errors = df["date"].isna().sum()
            if date_errors > 0:
                self.validation_results["warnings"].append(
                    f"⚠️  {date_errors} rows have invalid date format"
                )
            else:
                self.validation_results["info"].append("✅ All dates are valid")
            
            # Check if amount can be numeric
            pd.to_numeric(df["amount"], errors="coerce")
            amount_errors = df["amount"].isna().sum()
            if amount_errors > 0:
                self.validation_results["warnings"].append(
                    f"⚠️  {amount_errors} rows have invalid amount format"
                )
            else:
                self.validation_results["info"].append("✅ All amounts are numeric")
            
            # Check type column values
            invalid_types = ~df["type"].isin(self.VALID_TYPES)
            if invalid_types.any():
                bad_types = df[invalid_types]["type"].unique().tolist()
                self.validation_results["warnings"].append(
                    f"⚠️  Invalid transaction types found: {bad_types}. Valid types: {self.VALID_TYPES}"
                )
            else:
                self.validation_results["info"].append(
                    f"✅ All transaction types are valid: {self.VALID_TYPES}"
                )
                
        except Exception as e:
            self.validation_results["errors"].append(f"❌ Column type validation error: {str(e)}")
            self.validation_results["valid"] = False
    
    def validate_missing_values(self, df):
        """Check for missing/null values"""
        missing_data = df.isnull().sum()
        total_missing = missing_data.sum()
        
        if total_missing > 0:
            missing_info = "\n".join([
                f"  • {col}: {count} missing values"
                for col, count in missing_data[missing_data > 0].items()
            ])
            self.validation_results["warnings"].append(
                f"⚠️  Found {total_missing} missing values:\n{missing_info}"
            )
        else:
            self.validation_results["info"].append("✅ No missing values found")
    
    def validate_duplicates(self, df):
        """Check for duplicate rows"""
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            self.validation_results["warnings"].append(
                f"⚠️  Found {duplicates} duplicate rows"
            )
        else:
            self.validation_results["info"].append("✅ No duplicate rows found")
    
    def validate_amount_values(self, df):
        """Check amount values are reasonable"""
        try:
            amounts = pd.to_numeric(df["amount"], errors="coerce")
            zero_amounts = (amounts == 0).sum()
            if zero_amounts > 0:
                self.validation_results["warnings"].append(
                    f"⚠️  Found {zero_amounts} rows with zero amount"
                )
            
            negative_credits = ((df["type"] == "credit") & (amounts < 0)).sum()
            if negative_credits > 0:
                self.validation_results["warnings"].append(
                    f"⚠️  Found {negative_credits} negative credit amounts"
                )
            
            positive_debits = ((df["type"] == "debit") & (amounts > 0)).sum()
            if positive_debits > 0:
                self.validation_results["warnings"].append(
                    f"⚠️  Found {positive_debits} positive debit amounts (should typically be negative)"
                )
        except Exception as e:
            self.validation_results["warnings"].append(f"⚠️  Amount value check error: {str(e)}")
    
    def get_summary_stats(self, df):
        """Get summary statistics of data"""
        try:
            stats = {
                "total_rows": len(df),
                "date_range": {
                    "start": str(pd.to_datetime(df["date"], errors="coerce").min()),
                    "end": str(pd.to_datetime(df["date"], errors="coerce").max())
                },
                "credits": (df["type"] == "credit").sum(),
                "debits": (df["type"] == "debit").sum(),
                "total_income": pd.to_numeric(df[df["type"] == "credit"]["amount"], errors="coerce").sum(),
                "total_expenses": pd.to_numeric(df[df["type"] == "debit"]["amount"], errors="coerce").sum(),
            }
            return stats
        except Exception as e:
            return {"error": str(e)}
    
    def validate(self, df):
        """Run all validations"""
        self.validation_results = {
            "errors": [],
            "warnings": [],
            "info": [],
            "valid": True
        }
        
        if df.empty:
            self.validation_results["errors"].append("❌ CSV file is empty")
            self.validation_results["valid"] = False
            return self.validation_results
        
        if not self.validate_columns(df):
            return self.validation_results
        
        self.validate_column_types(df)
        self.validate_missing_values(df)
        self.validate_duplicates(df)
        self.validate_amount_values(df)
        
        if self.validation_results["errors"]:
            self.validation_results["valid"] = False
        
        return self.validation_results


def show_validation(API_BASE_URL):
    """Display data validation UI"""
    st.header("✅ Data Validation")
    
    st.markdown("""
    Upload your CSV file and validate it before processing. 
    Check for missing values, invalid formats, and data quality issues.
    """)
    
    # File uploader
    uploaded_file = st.file_uploader("Upload CSV file to validate", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)
            
            # Initialize validator
            validator = DataValidator()
            validation_results = validator.validate(df)
            stats = validator.get_summary_stats(df)
            
            # Display validation results
            with st.container():
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Data Summary")
                    if "error" not in stats:
                        st.metric("Total Rows", stats["total_rows"])
                        st.metric("Credit Transactions", stats["credits"])
                        st.metric("Debit Transactions", stats["debits"])
                
                with col2:
                    st.subheader("💰 Financial Summary")
                    if "error" not in stats:
                        st.metric("Total Income", f"₹ {stats['total_income']:,.2f}")
                        st.metric("Total Expenses", f"₹ {abs(stats['total_expenses']):,.2f}")
                        st.metric("Net Amount", f"₹ {(stats['total_income'] + stats['total_expenses']):,.2f}")
            
            st.divider()
            
            # Display validation messages
            st.subheader("🔍 Validation Results")
            
            # Info messages
            if validation_results["info"]:
                with st.container():
                    for msg in validation_results["info"]:
                        st.success(msg)
            
            # Warning messages
            if validation_results["warnings"]:
                with st.container():
                    for msg in validation_results["warnings"]:
                        st.warning(msg)
            
            # Error messages
            if validation_results["errors"]:
                with st.container():
                    for msg in validation_results["errors"]:
                        st.error(msg)
            
            st.divider()
            
            # Data preview
            st.subheader("👀 Data Preview")
            st.dataframe(df, use_container_width=True)
            
            # Display sample statistics
            st.subheader("📈 Column Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Column Types:**")
                st.dataframe(df.dtypes)
            
            with col2:
                st.write("**Missing Values:**")
                st.dataframe(df.isnull().sum())
            
            with col3:
                st.write("**Sample Amount Values:**")
                amounts = pd.to_numeric(df["amount"], errors="coerce").describe()
                st.dataframe(amounts)
            
            st.divider()
            
            # Validation status and next steps
            if validation_results["valid"]:
                st.success("✅ **Data validation passed!** This file is ready to upload.")
                if st.button("📤 Proceed to Upload", key="validate_upload"):
                    st.session_state.file_to_upload = uploaded_file
                    st.info("File saved! Go to Upload tab to complete the upload process.")
            else:
                st.error("❌ **Data validation failed.** Please fix the errors above before uploading.")
                st.info("💡 Tip: Review the errors and warnings, then upload a corrected CSV file.")
        
        except pd.errors.ParserError as e:
            st.error(f"❌ CSV parsing error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error validating file: {str(e)}")
    
    else:
        st.info("📁 Please upload a CSV file to begin validation")

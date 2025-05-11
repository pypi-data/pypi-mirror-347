import pandas as pd
import numpy as np
import inspect


# Set pandas display options
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pd.set_option("display.max_colwidth", 30)
pd.set_option("display.float_format", "{:,.2f}".format)


# Leading zeroes detection
def get_leading_zeros(df):
    """Get leading zeros in string columns of the DataFrame."""
    lz_cols = {}
    string_cols = df.select_dtypes(include=["object", "string"]).columns

    for col in string_cols:
        filtered_df = df[df[col].astype(str).fillna("").str.startswith("0")]
        if not filtered_df.empty:
            leading_zero_values = filtered_df[col].unique()
            lz_cols[col] = leading_zero_values.tolist()

    max_length = max(len(v) for v in lz_cols.values()) if lz_cols else 0
    for key in lz_cols.keys():
        while len(lz_cols[key]) < max_length:
            lz_cols[key].append(None)

    return pd.DataFrame(lz_cols)

# Getting string statistics
def get_str_stats(df):
    """Calculate statistics for string columns."""
    stats_data = {
        "Columns": [],
        "DTypes": [],
        "NaN": [],
        "Unique": [],
        "Duplicates": [],
        }
    
    for col in df.columns:
        unique_types = set()  
        for value in df[col]:
            if isinstance(value, float) and np.isnan(value):
                unique_types.add('NoneType')
            else:
                unique_types.add(type(value).__name__)

        stats_data["Columns"].append(col)
        stats_data["DTypes"].append(', '.join(unique_types))
        stats_data["NaN"].append(df[col].isna().sum())
                
        if any(isinstance(x, (list, dict, set)) for x in df[col].dropna()):
            df[col] = df[col].astype(str)

        stats_data["Unique"].append(len(df[col].unique()))
        stats_data["Duplicates"].append(df[col].duplicated().sum())
        
    return pd.DataFrame(stats_data)
        

    

# Getting outliers
def get_outliers(series):
    """Identify outliers in a Series using the IQR method."""
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return (series < lower_bound) | (series > upper_bound)

# Getting numeric statistics
def get_num_stats(df):
    """Calculate statistics for numeric columns."""
    stats_data = {
        "Columns": [],
        "Totals": [],
        "Min": [],
        "Max": [],
        "Mean": [],
        "Median": [],
        "STD": [],
        "STD (%)": [],
        "Outliers": [],
    }
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0).astype(float)
            stats_data["Columns"].append(col)
            stats_data["Min"].append(df[col].min())
            stats_data["Max"].append(df[col].max())
            stats_data["Mean"].append(df[col].mean())
            stats_data["Median"].append(df[col].median())
            stats_data["STD"].append(df[col].std())
            stats_data["STD (%)"].append(
                (df[col].std() / df[col].mean()) * 100
                if df[col].mean() != 0
                else np.nan
            )
            stats_data["Totals"].append(df[col].sum())
            stats_data["Outliers"].append(get_outliers(df[col]).sum())
    
    return pd.DataFrame(stats_data)


# Orchestrating function
def show(df):
    """Display statistics and leading zeros for the DataFrame."""
    try:
        # Getting the name of incoming df
        caller_frame = inspect.currentframe().f_back
        for name, obj in caller_frame.f_locals.items():
            if obj is df:
                display_name = name
        

        lz = get_leading_zeros(df)
        df_str_stats = get_str_stats(df)
        df_num_stats = get_num_stats(df)
        df_summary = pd.merge(df_str_stats, df_num_stats, on="Columns", how='left')
        
        print(f"{' ' * 100}")
        print(f"{'=' * 50} {display_name} {'=' * 50}")

        print("Leading zeros in columns\n")
        print(lz.head(3))

        print("\nGeneral stats\n")
        print(df_summary)
        

        print(f"Overall data frame length: {len(df)}")
    except Exception as error:
        return str(error)




# This is the overall code structure for the utility functions used in data processing.
# All data functions live here

import pandas as pd
import numpy as np

# Merge data
def merge_data(df_list):
    merged = df_list[0]
    for df in df_list[1:]:
        common = [col for col in merged.columns if col in df.columns and col != 'Player']
        df = df.drop(columns=common)
        merged = pd.merge(merged, df, on='Player', how='outer')
    merged = merged.drop_duplicates(subset=['Player', 'Squad'])
    return merged

# Calculate per 90 minutes
def calculate_per90(df):
    # Ensure '90s' is numeric
    df['90s'] = pd.to_numeric(df['90s'], errors='coerce')

    # Only use numeric columns (int64/float64), excluding specific ones
    excluded_cols = ['90s', 'Rk', 'Born']
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    numeric_cols = [col for col in numeric_cols if col not in excluded_cols]

    # Calculate per 90 values
    for col in numeric_cols:
        df[col + '_per90'] = np.where(df['90s'] > 0, (df[col] / df['90s']).round(2), 0)

    # Drop the original stat columns (not metadata)
    df = df.drop(columns=numeric_cols)

    return df


# Filter by 90s played
def filter_by_90s(df, min_90s=4.0):
    df['90s'] = pd.to_numeric(df['90s'], errors='coerce')
    return df[df['90s'] >= min_90s]

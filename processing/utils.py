# This is the overall code structure for the utility functions used in data processing.
# All data functions live here

import pandas as pd
import numpy as np
import os
import re


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
# def calculate_per90(df):
#     # Ensure '90s' is numeric
#     df['90s'] = pd.to_numeric(df['90s'], errors='coerce')

#     # Only use numeric columns (int64/float64), excluding specific ones
#     excluded_cols = ['90s', 'Rk', 'Born']
#     numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
#     numeric_cols = [col for col in numeric_cols if col not in excluded_cols]

#     # Calculate per 90 values
#     for col in numeric_cols:
#         df[col + '_per90'] = np.where(df['90s'] > 0, (df[col] / df['90s']).round(2), 0)

#     # Drop the original stat columns (not metadata)
#     df = df.drop(columns=numeric_cols)

#     return df

# def calculate_per90(df):
    
#     # Ensure '90s' is numeric
#     df['90s'] = pd.to_numeric(df['90s'], errors='coerce')

#     # Identify only raw integer columns (excluding '90s' itself)
#     excluded_cols = ['90s', 'Rk', 'Born', 'Age', 'Matches', 'Player', 'Nation', 'Pos', 'Squad']
#     raw_int_cols = [
#         col for col in df.columns
#         if col not in excluded_cols
#         and pd.api.types.is_numeric_dtype(df[col])
#         and (df[col].dropna() % 1 == 0).all()
#     ]

#     # Calculate per90 values
#     for col in raw_int_cols:
#         df[col + '_per90'] = np.where(df['90s'] > 0, (df[col] / df['90s']).round(2), 0)

#     # Drop the raw count columns
#     df = df.drop(columns=raw_int_cols)
#     return df

def calculate_per90(df):
    # Ensure 90s is numeric (and avoid divide-by-zero later)
    df['90s'] = pd.to_numeric(df.get('90s'), errors='coerce').fillna(0)

    # Columns never to convert
    excluded_cols = {'90s','Rk','Born','Age','Matches','Player','Nation','Pos','Squad'}

    # Exclude patterns: percentages, already per90, ratios, the 90s base, on/off, win%
    exclude_patterns = [
        r'%',          # any percentage column (Cmp%, Won%, etc.)
        r'per90',      # already per-90 columns
        r'/',          # ratios like G/Sh, Mn/Sub, etc.
        r'^90s$',      # the base itself
        r'On-Off',     # on/off diffs
        r'Won%$',      # win %
    ]
    exclude_re = re.compile('|'.join(exclude_patterns), flags=re.IGNORECASE)

    # Pick numeric columns that are not excluded by name or pattern
    candidate_cols = [
        c for c in df.columns
        if c not in excluded_cols
        and pd.api.types.is_numeric_dtype(df[c])
        and not exclude_re.search(c)
    ]

    # Compute per90 for those columns
    for c in candidate_cols:
        df[f'{c}_per90'] = np.where(df['90s'] > 0, (df[c] / df['90s']).round(2), 0)

    return df


# Filter by 90s played
def filter_by_90s(df, min_90s=4.0):
    df['90s'] = pd.to_numeric(df['90s'], errors='coerce')
    return df[df['90s'] >= min_90s]

# Reformat for PowerBI
def reformat_powerbi(df, path):
    df.to_csv(path, sep=';', decimal=',', index=False)
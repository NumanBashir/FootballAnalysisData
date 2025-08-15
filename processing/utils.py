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
        r'%',             # any percentage column (Cmp%, Won%, etc.)
        r'per90',         # already per-90 columns
        r'[A-Za-z]/[A-Za-z]',  # ratios like G/Sh, Mn/Sub, etc.
        r'^90s$',         # the base itself
        r'On-Off',        # on/off diffs
        r'Won%$',         # win %
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


def player_league_average_only(df):
    """
    Returns a DataFrame containing only the league average row for all numeric columns
    in the players list, excluding MP, Starts, Min, and 90s. 
    Rounds to 2 decimals.
    """
    # Ensure column names are unique
    df = df.loc[:, ~df.columns.duplicated()]

    exclude_cols = {'MP', 'Starts', 'Min', '90s'}

    numeric_cols = []
    for col in df.columns:
        if col not in exclude_cols and col != "Player":
            df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')  # ensure numeric
            if pd.api.types.is_numeric_dtype(df[col]):
                numeric_cols.append(col)

    avg_row = {}
    for col in df.columns:
        if col == "Player":
            avg_row[col] = "All players"
        elif col in numeric_cols:
            avg_row[col] = round(df[col].mean(), 2)
        else:
            avg_row[col] = None

    return pd.DataFrame([avg_row])

def player_league_average_by_position(df, positions):
    """
    Returns a DataFrame with league averages for only the players whose 'Pos' matches
    any of the positions in the given list.

    Parameters
    ----------
    df : pandas.DataFrame
        Player stats DataFrame with a 'Pos' column.
    positions : list[str]
        List of position strings to include (e.g., ["DF", "MF, FW"]).

    Returns
    -------
    pandas.DataFrame
        Single-row DataFrame with averages for the filtered players.
    """
    # Filter players by given positions
    filtered_df = df[df['Pos'].isin(positions)].copy()

    if filtered_df.empty:
        raise ValueError(f"No players found for positions: {positions}")

    # Columns we should never average (metadata or IDs)
    do_not_avg = {
        'Rk', 'Player', 'Nation', 'Pos', 'Squad',
        'Matches', 'Born', 'MP', 'Starts', 'Min', '90s'
    }

    avg_row = {}

    for col in filtered_df.columns:
        if col == 'Player':
            avg_row[col] = f"Avg for {', '.join(positions)}"
        elif col == 'Squad':
            avg_row[col] = "Selected teams"
        elif col in do_not_avg:
            avg_row[col] = None
        else:
            col_num = pd.to_numeric(filtered_df[col], errors='coerce')
            if not col_num.isna().all():
                avg_row[col] = round(col_num.mean(), 2)
            else:
                avg_row[col] = None

    return pd.DataFrame([avg_row])

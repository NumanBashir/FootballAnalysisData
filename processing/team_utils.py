import pandas as pd
import numpy as np
import re

def merge_team_tables(df_list):
    """
    Merge team tables horizontally on 'Squad'.
    """
    valid_tables = []
    for df in df_list:
        if 'Squad' in df.columns:
            valid_tables.append(df)
        else:
            print("⚠️ Skipping table without 'Squad' column")

    if not valid_tables:
        raise ValueError("❌ No tables with a 'Squad' column were found")

    merged = valid_tables[0]
    for df in valid_tables[1:]:
        common_cols = [col for col in merged.columns if col in df.columns and col != 'Squad']
        df = df.drop(columns=common_cols)
        merged = pd.merge(merged, df, on='Squad', how='outer')

    return merged.drop_duplicates(subset=['Squad'])

import pandas as pd

def league_average_only(df):
    """
    Returns a DataFrame containing only the league average row for all numeric columns,
    excluding MP, Starts, Min. Rounds to 1 decimal.
    """
    # Ensure column names are unique
    df = df.loc[:, ~df.columns.duplicated()]

    exclude_cols = {'MP', 'Starts', 'Min'}

    numeric_cols = []
    for col in df.columns:
        if col not in exclude_cols and col != "Squad":
            df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')  # ensure numeric
            if pd.api.types.is_numeric_dtype(df[col]):
                numeric_cols.append(col)

    avg_row = {}
    for col in df.columns:
        if col == "Squad":
            avg_row[col] = "All teams"
        elif col in numeric_cols:
            avg_row[col] = round(df[col].mean(), 2)
        else:
            avg_row[col] = None

    return pd.DataFrame([avg_row])


def team_calculate_per90(df):
    # --- Step 1: Deduplicate column names ---
    # Strip spaces first
    df.columns = df.columns.str.strip()

    # Add suffixes to duplicate names
    seen = {}
    new_cols = []
    for col in df.columns:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")  # e.g. Gls_2
        else:
            seen[col] = 0
            new_cols.append(col)
    df.columns = new_cols

    # --- Step 2: Ensure 90s column is numeric ---
    df['90s'] = pd.to_numeric(df.get('90s'), errors='coerce').fillna(0)

    # --- Step 3: Columns never to convert ---
    excluded_cols = {
        'Squad', '# Pl', 'Age', 'Poss', 'MP', 'Starts', 'Min', '90s'
    }

    # --- Step 4: Patterns to exclude ---
    exclude_patterns = [
        r'%',           # percentages
        r'per90',       # already per-90
        r'/90',         # already per-90
        r'^90s$',       # base column
        r'On-Off',      # on/off diffs
        r'Won%$',       # win %
    ]
    exclude_re = re.compile('|'.join(exclude_patterns), flags=re.IGNORECASE)

    raw_cols = []

    # --- Step 5: Detect numeric columns for per90 ---
    for col in df.columns:
        if col in excluded_cols or exclude_re.search(str(col)):
            continue

        try:
            col_data = pd.to_numeric(df[col], errors='coerce')
            if not col_data.isna().all():
                raw_cols.append(col)
        except Exception:
            continue

    print(f"🔍 Converting to per90: {raw_cols}")

    # --- Step 6: Vectorized per90 calculation (avoid fragmentation) ---
    per90_df = pd.DataFrame(index=df.index)
    for col in raw_cols:
        per90_df[f"{col}_per90"] = np.where(
            df['90s'] > 0,
            (pd.to_numeric(df[col], errors='coerce') / df['90s']).round(2),
            0
        )

    # --- Step 7: Concatenate new columns in one go to avoid fragmentation ---
    df = pd.concat([df, per90_df], axis=1)

    return df



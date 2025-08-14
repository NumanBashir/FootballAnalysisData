import pandas as pd

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
            avg_row[col] = round(df[col].mean(), 1)
        else:
            avg_row[col] = None

    return pd.DataFrame([avg_row])



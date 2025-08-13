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

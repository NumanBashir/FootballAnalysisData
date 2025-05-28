import pandas as pd

def merge_player_tables(df_list):
    """
    Merge player tables horizontally on 'Season', ensuring each row represents one season.
    Skips any tables that do not contain a 'Season' column.
    """
    valid_tables = []
    for df in df_list:
        if 'Season' in df.columns:
            df['Season'] = df['Season'].astype(str)
            valid_tables.append(df)
        else:
            print("⚠️ Skipping table without 'Season' column")

    if not valid_tables:
        raise ValueError("❌ No tables with a 'Season' column were found")

    merged = valid_tables[0]
    for df in valid_tables[1:]:
        # Drop overlapping columns (except 'Season') before merging
        common_cols = [col for col in merged.columns if col in df.columns and col != 'Season']
        df = df.drop(columns=common_cols)
        merged = pd.merge(merged, df, on='Season', how='outer')

    return merged.drop_duplicates()

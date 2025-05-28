import pandas as pd
import numpy as np

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

def calculate_per90(df):
    import numpy as np
    import pandas as pd

    df['90s'] = pd.to_numeric(df['90s'], errors='coerce')

    excluded_cols = {
        'Player', 'Squad', 'Season', 'Comp', 'Age', 'Nation', 'Pos', 'Born', 'Team', 'Matches', '90s'
    }

    raw_cols = []

    for col in df.columns:
        if (
            col in excluded_cols or
            '_per90' in col.lower() or
            '%' in col or
            col.strip().endswith('%')
        ):
            continue

        try:
            col_data = pd.to_numeric(df[col], errors='coerce')
            if not col_data.isna().all():
                raw_cols.append(col)
        except:
            continue

    print(f"🔍 Converting to per90 and dropping originals: {raw_cols}")

    for col in raw_cols:
        df[col + '_per90'] = np.where(
            df['90s'] > 0,
            (pd.to_numeric(df[col], errors='coerce') / df['90s']).round(2),
            0
        )

    df.drop(columns=raw_cols, inplace=True)
    return df




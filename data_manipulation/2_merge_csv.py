import pandas as pd

# Load the CSVs
df1 = pd.read_csv("Bundesliga24_25/players_possession.csv")
df2 = pd.read_csv("Bundesliga24_25/sca_gca.csv")

# Ensure player names are clean (optional but recommended)
df1['Player'] = df1['Player'].str.strip()
df2['Player'] = df2['Player'].str.strip()

# Get overlapping columns (excluding 'Player')
common_cols = [col for col in df1.columns if col in df2.columns and col != 'Player']

# Drop overlapping columns from df2 (except 'Player')
df2_cleaned = df2.drop(columns=common_cols)

# Merge the cleaned dataframes
merged_df = pd.merge(df1, df2_cleaned, on='Player', how='outer')

# Remove duplicates based on 'Player' and 'Squad'
merged_df = merged_df.drop_duplicates(subset=['Player', 'Squad'])

# Save the result
merged_df.to_csv("possession_sca_gca.csv", index=False)
print("Merged to 'possession_sca_gca.csv' ✅")

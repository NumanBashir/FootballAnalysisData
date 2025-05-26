import pandas as pd

df = pd.read_csv("Bundesliga24_25/per90_possession_sca_gca.csv") # TODO: use correct file name

# Ensure '90s' is numeric
df['90s'] = pd.to_numeric(df['90s'], errors='coerce')

# Filter: keep only rows where 90s >= 4.0
df = df[df['90s'] >= 4.0] # TODO: change number as desired

df.to_csv("Bundesliga24_25/450min_above_possession_sca_gca_per90.csv", index=False) # TODO: change name
print("Rows with less than 4.0 '90s' removed ✅")

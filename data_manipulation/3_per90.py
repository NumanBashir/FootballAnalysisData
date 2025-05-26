import pandas as pd
import numpy as np

# Load merged data
df = pd.read_csv("input_data/championship_merged.csv")

# Ensure '90s' column is float for accurate division
df['90s'] = pd.to_numeric(df['90s'], errors='coerce')

# Identify numeric columns (excluding '90s', 'Rk', and 'Born')
excluded_cols = ['90s', 'Rk', 'Born']
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
numeric_cols = [col for col in numeric_cols if col not in excluded_cols]

# Calculate per 90 values
for col in numeric_cols:
    df[col + '_per90'] = np.where(df['90s'] > 0, (df[col] / df['90s']).round(2), 0) # Avoid division by zero for players with 0 '90s'

# Optional: drop original columns if you only want per90 columns
df = df.drop(columns=numeric_cols)

# Save the updated DataFrame
df.to_csv("test.csv", index=False)
print("Per 90 stats saved ✅")

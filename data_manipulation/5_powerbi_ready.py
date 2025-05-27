import pandas as pd

# Step 1: Load your original CSV
input_path = "output\Bundesliga_24_25\\450min_above_possession_sca_gca_per90.csv"  # Replace with your actual file name
df = pd.read_csv(input_path)

# Step 2: Export with ; separator and , as decimal (Power BI–friendly for EU locales)
output_path = "450min_above_possession_sca_gca_per90_powerbi.csv"
df.to_csv(output_path, sep=';', decimal=',', index=False)

print(f"✅ Saved Power BI-ready file as: {output_path}")

import pandas as pd
from processing.player_utils import calculate_per90

df = pd.read_csv("output/player/test_merged.csv")
df = calculate_per90(df)
df.to_csv("output/player/per90.csv", index=False)

from processing.player_utils import filter_by_season

# Example season string — adjust if needed
target_season = "2023-2024"

df = filter_by_season(df, target_season)

# Save filtered output to verify
df.to_csv("output/player_stats_2024_2025.csv", index=False)

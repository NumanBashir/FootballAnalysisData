import pandas as pd
from processing.player_utils import calculate_per90

df = pd.read_csv("output/player/test_merged.csv")
df = calculate_per90(df)
df.to_csv("output/player/per90.csv", index=False)

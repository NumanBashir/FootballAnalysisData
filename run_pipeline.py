# Main script that runs everything in order

from scraping.fbref_scraper import scrape_table
from processing.utils import merge_data, calculate_per90, filter_by_90s, reformat_powerbi
import pandas as pd

# Step 1: Scrape (or manually save and load)
# tables = [
#     scrape_table("https://fbref.com/en/comps/20/gca/Bundesliga-Stats", "stats_gca"), # url, table_id
#     pd.read_csv("input_data/gca1.csv"),  # Example of manual file 
# ]

# Remember to change URL and table_id
tables = [
    scrape_table("https://fbref.com/en/comps/9/2024-2025/stats/2024-2025-Premier-League-Stats", "stats_standard"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/shooting/2024-2025-Premier-League-Stats", "stats_shooting"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/passing/2024-2025-Premier-League-Stats", "stats_passing"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/passing_types/2024-2025-Premier-League-Stats", "stats_passing_types"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/gca/2024-2025-Premier-League-Stats", "stats_gca"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/defense/2024-2025-Premier-League-Stats", "stats_defense"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/possession/2024-2025-Premier-League-Stats", "stats_possession"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/playingtime/2024-2025-Premier-League-Stats", "stats_playing_time"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/misc/2024-2025-Premier-League-Stats", "stats_misc"),
]

# GK tables
# tables = [
#     scrape_table("https://fbref.com/en/comps/32/keepers/Primeira-Liga-Stats", "stats_keeper"),
#     scrape_table("https://fbref.com/en/comps/32/keepersadv/Primeira-Liga-Stats", "stats_keeper_adv"),
# ]

# Step 2: Merge
merge_data(tables).to_csv("output/PremierLeague_24_25/merged_PremierLeague_24_25.csv", index=False)
df = pd.read_csv("output/PremierLeague_24_25/merged_PremierLeague_24_25.csv")

# Step 3: Filter by 90s played (valid data > 5.0 / 450 mins)
df = filter_by_90s(df, min_90s=5.0)
df.to_csv("output/PremierLeague_24_25/filter_PremierLeague_24_25.csv", index=False)

# Step 4: Reformat for better interpret for PowerBI
reformat_powerbi(df, "output/PremierLeague_24_25/reformat_PremierLeague_24_25.csv")


### EXTRA STEP --> Total + per90
# This is a BIG table with both total and per90 --> Comment out this if don't need --> Use PowerBI to calculate per90
df = calculate_per90(df)
df.to_csv("output/PremierLeague_24_25/BIG_per90_PremierLeague_24_25.csv", index=False)
reformat_powerbi(df, "output/PremierLeague_24_25/BIG_reformat_PremierLeague_24_25.csv")


print("Pipeline complete ✅")

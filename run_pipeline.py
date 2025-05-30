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
    scrape_table("https://fbref.com/en/comps/13/stats/Ligue-1-Stats", "stats_standard"),
    scrape_table("https://fbref.com/en/comps/13/shooting/Ligue-1-Stats", "stats_shooting"),
    scrape_table("https://fbref.com/en/comps/13/passing/Ligue-1-Stats", "stats_passing"),
    scrape_table("https://fbref.com/en/comps/13/passing_types/Ligue-1-Stats", "stats_passing_types"),
    scrape_table("https://fbref.com/en/comps/13/gca/Ligue-1-Stats", "stats_gca"),
    scrape_table("https://fbref.com/en/comps/13/defense/Ligue-1-Stats", "stats_defense"),
    scrape_table("https://fbref.com/en/comps/13/possession/Ligue-1-Stats", "stats_possession"),
    scrape_table("https://fbref.com/en/comps/13/playingtime/Ligue-1-Stats", "stats_playing_time"),
    scrape_table("https://fbref.com/en/comps/13/misc/Ligue-1-Stats", "stats_misc"),
]

# Step 2: Merge
merge_data(tables).to_csv("output/Ligue1_24_25/merged_ligue_24_25.csv", index=False)
df = pd.read_csv("output/Ligue1_24_25/merged_ligue_24_25.csv")

# Step 3: Per 90
df = calculate_per90(df)
df.to_csv("output/Ligue1_24_25/per90_ligue_24_25.csv", index=False)

# Step 4: Filter by 90s played
df = filter_by_90s(df, min_90s=5.0)
df.to_csv("output/Ligue1_24_25/filter_ligue_24_25.csv", index=False)

# Step 5: Reformat for better interpret for PowerBI 
reformat_powerbi(df, "output/Ligue1_24_25/reformat_ligue_24_25.csv")

print("Pipeline complete ✅")

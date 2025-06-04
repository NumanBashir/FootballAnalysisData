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
    scrape_table("https://fbref.com/en/comps/50/stats/Danish-Superliga-Stats", "stats_standard"),
    scrape_table("https://fbref.com/en/comps/50/shooting/Danish-Superliga-Stats", "stats_shooting"),
    # scrape_table("https://fbref.com/en/comps/32/passing/Primeira-Liga-Stats", "stats_passing"),
    # scrape_table("https://fbref.com/en/comps/32/passing_types/Primeira-Liga-Stats", "stats_passing_types"),
    # scrape_table("https://fbref.com/en/comps/32/gca/Primeira-Liga-Stats", "stats_gca"),
    # scrape_table("https://fbref.com/en/comps/32/defense/Primeira-Liga-Stats", "stats_defense"),
    # scrape_table("https://fbref.com/en/comps/32/possession/Primeira-Liga-Stats", "stats_possession"),
    scrape_table("https://fbref.com/en/comps/50/playingtime/Danish-Superliga-Stats", "stats_playing_time"),
    scrape_table("https://fbref.com/en/comps/50/misc/Danish-Superliga-Stats", "stats_misc"),
]

# GK tables
# tables = [
#     scrape_table("https://fbref.com/en/comps/32/keepers/Primeira-Liga-Stats", "stats_keeper"),
#     scrape_table("https://fbref.com/en/comps/32/keepersadv/Primeira-Liga-Stats", "stats_keeper_adv"),
# ]

# Step 2: Merge
merge_data(tables).to_csv("output/Superliga_24_25/merged_Superliga_24_25.csv", index=False)
df = pd.read_csv("output/Superliga_24_25/merged_Superliga_24_25.csv")

# Step 3: Filter by 90s played (valid data > 5.0 / 450 mins)
df = filter_by_90s(df, min_90s=3.0)
df.to_csv("output/Superliga_24_25/filter_Superliga_24_25.csv", index=False)

# Step 4: Per 90 --> If don't want per90 stats but whole number then comment out this
df = calculate_per90(df)
df.to_csv("output/Superliga_24_25/per90_Superliga_24_25.csv", index=False)

# Step 5: Reformat for better interpret for PowerBI 
reformat_powerbi(df, "output/Superliga_24_25/reformat_Superliga_24_25.csv")

print("Pipeline complete ✅")

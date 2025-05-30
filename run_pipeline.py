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
    scrape_table("https://fbref.com/en/comps/9/stats/Premier-League-Stats", "stats_standard"),
    scrape_table("https://fbref.com/en/comps/9/shooting/Premier-League-Stats", "stats_shooting"),
    scrape_table("https://fbref.com/en/comps/9/passing/Premier-League-Stats", "stats_passing"),
    scrape_table("https://fbref.com/en/comps/9/passing_types/Premier-League-Stats", "stats_passing_types"),
    scrape_table("https://fbref.com/en/comps/9/gca/Premier-League-Stats", "stats_gca"),
    scrape_table("https://fbref.com/en/comps/9/defense/Premier-League-Stats", "stats_defense"),
    scrape_table("https://fbref.com/en/comps/9/possession/Premier-League-Stats", "stats_possession"),
    scrape_table("https://fbref.com/en/comps/9/playingtime/Premier-League-Stats", "stats_playing_time"),
    scrape_table("https://fbref.com/en/comps/9/misc/Premier-League-Stats", "stats_misc"),
]

# Step 2: Merge
merge_data(tables).to_csv("output/PremierLeague_24_25/merged_premier_league_24_25.csv", index=False)
df = pd.read_csv("output/PremierLeague_24_25/merged_premier_league_24_25.csv")

# Step 3: Per 90
df = calculate_per90(df)
df.to_csv("output/PremierLeague_24_25/per90_premier_league_24_25.csv", index=False)

# Step 4: Filter by 90s played
df = filter_by_90s(df, min_90s=5.0)
df.to_csv("output/PremierLeague_24_25/filter_premier_league_24_25.csv", index=False)

# Step 5: Reformat for better interpret for PowerBI 
reformat_powerbi(df, "output/PremierLeague_24_25/reformat_premier_league_24_25.csv")

print("Pipeline complete ✅")

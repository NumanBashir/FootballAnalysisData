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
    scrape_table("https://fbref.com/en/comps/11/stats/Serie-A-Stats", "stats_standard"),
    scrape_table("https://fbref.com/en/comps/11/shooting/Serie-A-Stats", "stats_shooting"),
    scrape_table("https://fbref.com/en/comps/11/passing/Serie-A-Stats", "stats_passing"),
    scrape_table("https://fbref.com/en/comps/11/passing_types/Serie-A-Stats", "stats_passing_types"),
    scrape_table("https://fbref.com/en/comps/11/gca/Serie-A-Stats", "stats_gca"),
    scrape_table("https://fbref.com/en/comps/11/defense/Serie-A-Stats", "stats_defense"),
    scrape_table("https://fbref.com/en/comps/11/possession/Serie-A-Stats", "stats_possession"),
    scrape_table("https://fbref.com/en/comps/11/playingtime/Serie-A-Stats", "stats_playing_time"),
    scrape_table("https://fbref.com/en/comps/11/misc/Serie-A-Stats", "stats_misc"),
]

# Step 2: Merge
merge_data(tables).to_csv("output/SerieA_24_25/merged_serie_a_24_25.csv", index=False)
df = pd.read_csv("output/SerieA_24_25/merged_serie_a_24_25.csv")

# Step 3: Per 90
df = calculate_per90(df)
df.to_csv("output/SerieA_24_25/per90_serie_a_24_25.csv", index=False)

# Step 4: Filter by 90s played
df = filter_by_90s(df, min_90s=5.0)
df.to_csv("output/SerieA_24_25/filter_serie_a_24_25.csv", index=False)

# Step 5: Reformat for better interpret for PowerBI 
reformat_powerbi(df, "output/SerieA_24_25/reformat_serie_a_24_25.csv")

print("Pipeline complete ✅")

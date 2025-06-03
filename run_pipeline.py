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
    scrape_table("https://fbref.com/en/comps/23/stats/Eredivisie-Stats", "stats_standard"),
    scrape_table("https://fbref.com/en/comps/23/shooting/Eredivisie-Stats", "stats_shooting"),
    scrape_table("https://fbref.com/en/comps/23/passing/Eredivisie-Stats", "stats_passing"),
    scrape_table("https://fbref.com/en/comps/23/passing_types/Eredivisie-Stats", "stats_passing_types"),
    scrape_table("https://fbref.com/en/comps/23/gca/Eredivisie-Stats", "stats_gca"),
    scrape_table("https://fbref.com/en/comps/23/defense/Eredivisie-Stats", "stats_defense"),
    scrape_table("https://fbref.com/en/comps/23/possession/Eredivisie-Stats", "stats_possession"),
    scrape_table("https://fbref.com/en/comps/23/playingtime/Eredivisie-Stats", "stats_playing_time"),
    scrape_table("https://fbref.com/en/comps/23/misc/Eredivisie-Stats", "stats_misc"),
]

# Step 2: Merge
merge_data(tables).to_csv("output/Eredivisie_24_25/merged_eredivisie_24_25.csv", index=False)
df = pd.read_csv("output/Eredivisie_24_25/merged_eredivisie_24_25.csv")

# Step 3: Per 90
df = calculate_per90(df)
df.to_csv("output/Eredivisie_24_25/per90_eredivisie_24_25.csv", index=False)

# Step 4: Filter by 90s played (min. 450 mins)
df = filter_by_90s(df, min_90s=5.0)
df.to_csv("output/Eredivisie_24_25/filter_eredivisie_24_25.csv", index=False)

# Step 5: Reformat for better interpret for PowerBI 
reformat_powerbi(df, "output/Eredivisie_24_25/reformat_eredivisie_24_25.csv")

print("Pipeline complete ✅")

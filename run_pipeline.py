# Main script that runs everything in order

from scraping.fbref_scraper import scrape_table
from processing.utils import merge_data, calculate_per90, filter_by_90s
import pandas as pd

# Step 1: Scrape (or manually save and load)
# tables = [
#     scrape_table("https://fbref.com/en/comps/20/gca/Bundesliga-Stats", "stats_gca"), # url, table_id
#     pd.read_csv("input_data/gca1.csv"),  # Example of manual file 
# ]

# Remember to change URL and table_id
tables = [
    scrape_table("https://fbref.com/en/comps/10/possession/Championship-Stats", "stats_possession"),
    scrape_table("https://fbref.com/en/comps/10/gca/Championship-Stats", "stats_gca"),
]

# Step 2: Merge
merge_data(tables).to_csv("output\Championship_24_25\merged.csv", index=False)
merged_df = pd.read_csv("output\Championship_24_25\merged.csv")

# Step 3: Per 90
per90_df = calculate_per90(merged_df)
per90_df.to_csv("output\Championship_24_25\per90.csv", sep=';', decimal=',', index=False)

# Step 4: Filter by 90s played
filtered_df = filter_by_90s(per90_df, min_90s=5.0)
filtered_df.to_csv("output\Championship_24_25\\filter.csv", sep=';', decimal=',', index=False)

print("Pipeline complete ✅")

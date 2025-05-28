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
    scrape_table("https://fbref.com/en/comps/10/possession/Championship-Stats", "stats_possession"),
    scrape_table("https://fbref.com/en/comps/10/gca/Championship-Stats", "stats_gca"),
]

# Step 2: Merge
merge_data(tables).to_csv("output\Championship_24_25\merged.csv", index=False)
df = pd.read_csv("output\Championship_24_25\merged.csv")

# Step 3: Per 90
df = calculate_per90(df)
df.to_csv("output\Championship_24_25\per90.csv", index=False)

# Step 4: Filter by 90s played
df = filter_by_90s(df, min_90s=5.0)
df.to_csv("output\Championship_24_25\\filter.csv", index=False)

# Step 5: Reformat for better interpret for PowerBI 
reformat_powerbi(df, "output/Championship_24_25/final_powerbi.csv")

print("Pipeline complete ✅")

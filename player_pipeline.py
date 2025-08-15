from scraping.player_scraper import scrape_player_table
from processing.player_utils import merge_player_tables, calculate_per90, filter_by_season
from processing.utils import reformat_powerbi
import pandas as pd
import time, random

# Step 1: Scrape player tables
url = "https://fbref.com/en/players/dc62b55d/Matheus-Cunha"

# Define all table IDs you want to scrape
table_ids = [
    "stats_standard_dom_lg", "stats_shooting_dom_lg", "stats_passing_dom_lg",
    "stats_passing_types_dom_lg", "stats_gca_dom_lg", "stats_defense_dom_lg",
    "stats_possession_dom_lg", "stats_playing_time_dom_lg", "stats_misc_dom_lg"
]

# Scrape all tables
tables = []
for i, table_id in enumerate(table_ids, start=1):
    df = scrape_player_table(url, table_id)
    if df is not None:
        print(f"✅ Table {i}: {df.shape} — {table_id}")
        tables.append(df)
    else:
        print(f"❌ Table {i} not found: {table_id}")

    time.sleep(random.uniform(3, 6))

# Step 2: Merge
df = merge_player_tables(tables)
df.to_csv("player_scout_reports/player/matheus_cunha/1_merged.csv", index=False)

# Step 3: Calculate per90
df = pd.read_csv("player_scout_reports/player/matheus_cunha/1_merged.csv")
df = calculate_per90(df)
df.to_csv("player_scout_reports/player/matheus_cunha/2_per90.csv", index=False)

# Step 4: Filter by seasons
df = filter_by_season(df, ["2024-2025"])
df.to_csv("player_scout_reports/player/matheus_cunha/3_season.csv", index=False)

# Step 5: Reformat for Power BI
reformat_powerbi(df, "player_scout_reports/player/matheus_cunha/final_powerbi.csv")

print("🚀 Player pipeline complete!")
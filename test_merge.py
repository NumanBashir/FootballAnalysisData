from scraping.player_scraper import scrape_player_table
from processing.player_utils import merge_player_tables

# Player URL (Florian Wirtz example)
url = "https://fbref.com/en/players/e7fcf289/Florian-Wirtz"

# List of table IDs to scrape
table_ids = [
    "stats_standard_dom_lg", "stats_shooting_dom_lg", "stats_passing_dom_lg",
    "stats_passing_types_dom_lg", "stats_gca_dom_lg", "stats_defense_dom_lg",
    "stats_possession_dom_lg", "stats_playing_time_dom_lg", "stats_misc_dom_lg"
]

# Step 1: Scrape all tables
tables = []
for i, table_id in enumerate(table_ids, start=1):
    df = scrape_player_table(url, table_id)
    if df is not None:
        print(f"✅ Table {i}: {df.shape} — {table_id}")
        tables.append(df)
    else:
        print(f"❌ Table {i} not found: {table_id}")

# Step 2: Merge tables
merged = merge_player_tables(tables)
print("✅ Merge complete. Result shape:", merged.shape)

# Optional: Save to CSV to inspect
merged.to_csv("output/player/test_merged.csv", index=False)
print("📄 Saved merged CSV to: output/player/test_merged.csv")

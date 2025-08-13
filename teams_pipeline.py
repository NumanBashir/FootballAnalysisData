from scraping.team_scraper import scrape_team_table
from processing.team_utils import merge_team_tables, league_average_only
from processing.utils import calculate_per90, reformat_powerbi
import pandas as pd

url = "https://fbref.com/en/comps/9/2024-2025/2024-2025-Premier-League-Stats"

table_ids = [
    "stats_squads_standard_for", "stats_squads_keeper_for", "stats_squads_keeper_adv_for",
    "stats_squads_shooting_for", "stats_squads_passing_for", "stats_squads_passing_types_for",
    "stats_squads_gca_for", "stats_squads_defense_for", "stats_squads_possession_for", 
    "stats_squads_playing_time_for", "stats_squads_misc_for"
]


# Step 1: Scrape
tables = []
for i, table_id in enumerate(table_ids, start=1):
    df = scrape_team_table(url, table_id)
    if df is not None:
        print(f"✅ Table {i}: {df.shape} — {table_id}")
        tables.append(df)
    else:
        print(f"❌ Table {i} not found: {table_id}")


# Step 2: Merge
df = merge_team_tables(tables)
df.to_csv("team_output/PremierLeague_24_25/team_merged_PremierLeague_24_25.csv", index=False)

# Step 3: Get only the league average
df_avg = league_average_only(df)
df_avg.to_csv("team_output/PremierLeague_24_25/team_league_average_24_25.csv", index=False)

print("Team pipeline complete ✅")
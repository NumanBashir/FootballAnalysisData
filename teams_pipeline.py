from scraping.team_scraper import scrape_team_table
from processing.team_utils import merge_team_tables, league_average_only, team_calculate_per90
from processing.utils import reformat_powerbi
import pandas as pd
import time, random


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

    time.sleep(random.uniform(3, 6))


# Step 2: Merge
df = merge_team_tables(tables)
df.to_csv("team_output/PremierLeague_24_25/team_merged_PremierLeague_24_25.csv", index=False)

# Step 3: Get ONLY the league average
df_avg = league_average_only(df)
# df_avg.to_csv("team_output/PremierLeague_24_25/team_league_average_24_25.csv", index=False)

# OPT: Reindex to match the original DataFrame columns and append the league average to the merged DataFrame, then save final CSV with league average included
df_avg = df_avg.reindex(columns=df.columns)
df_with_avg = pd.concat([df, df_avg], ignore_index=True)
# df_with_avg.to_csv("team_output/PremierLeague_24_25/team_merged_with_avg_PremierLeague_24_25.csv", index=False)

reformat_powerbi(df_with_avg, "team_output/PremierLeague_24_25/final_team_merged_with_avg_PremierLeague_24_25.csv")

# Step 4: Calculate team per90 stats
df_team_per90 = team_calculate_per90(df)
# df_team_per90.to_csv("team_output/PremierLeague_24_25/team_per90_PremierLeague_24_25.csv", index=False)

# Step 5: Get ONLY league average per 90
df_avg_per90 = league_average_only(df_team_per90)
# df_avg_per90.to_csv("team_output/PremierLeague_24_25/team_league_average_per90_24_25.csv", index=False)

# OPT: Append the league average per90 to the average per90, then save final CSV with league average included
df_avg_per90 = df_avg_per90.reindex(columns=df_team_per90.columns)
df_per90_with_avg = pd.concat([df_team_per90, df_avg_per90], ignore_index=True)
# df_per90_with_avg.to_csv("team_output/PremierLeague_24_25/team_per90_with_avg_PremierLeague_24_25.csv", index=False)

# Step 6: Reformat for Power BI (make sure to use the correct DataFrame)
reformat_powerbi(df_per90_with_avg, "team_output/PremierLeague_24_25/final_team_per90_with_league_avg_per90_PremierLeague_24_25.csv")

print("Team pipeline complete ✅")
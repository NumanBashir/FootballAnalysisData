# Main script that runs everything in order

from scraping.fbref_scraper import scrape_table
from processing.utils import merge_data, calculate_per90, filter_by_90s, reformat_powerbi, player_league_average_only, player_league_average_by_position
import pandas as pd

# Step 1: Scrape (or manually save and load)
# tables = [
#     scrape_table("https://fbref.com/en/comps/20/gca/Bundesliga-Stats", "stats_gca"), # url, table_id
#     pd.read_csv("input_data/gca1.csv"),  # Example of manual file 
# ]

# Remember to change URL and table_id
tables = [
    scrape_table("https://fbref.com/en/comps/9/2024-2025/stats/2024-2025-Premier-League-Stats", "stats_standard"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/shooting/2024-2025-Premier-League-Stats", "stats_shooting"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/passing/2024-2025-Premier-League-Stats", "stats_passing"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/passing_types/2024-2025-Premier-League-Stats", "stats_passing_types"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/gca/2024-2025-Premier-League-Stats", "stats_gca"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/defense/2024-2025-Premier-League-Stats", "stats_defense"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/possession/2024-2025-Premier-League-Stats", "stats_possession"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/playingtime/2024-2025-Premier-League-Stats", "stats_playing_time"),
    scrape_table("https://fbref.com/en/comps/9/2024-2025/misc/2024-2025-Premier-League-Stats", "stats_misc"),
]

# GK tables
# tables = [
#     scrape_table("https://fbref.com/en/comps/32/keepers/Primeira-Liga-Stats", "stats_keeper"),
#     scrape_table("https://fbref.com/en/comps/32/keepersadv/Primeira-Liga-Stats", "stats_keeper_adv"),
# ]

# Merge into one DataFrame for ALL players
merge_data(tables).to_csv("output/PremierLeague_24_25/merged_PremierLeague_24_25.csv", index=False)
df = pd.read_csv("output/PremierLeague_24_25/merged_PremierLeague_24_25.csv")

# Filter by 90s played (valid data > 5.0 / 450 mins)
df = filter_by_90s(df, min_90s=5.0) # This filters the DataFrame to only include players with more than 5 matches played
# df.to_csv("output/PremierLeague_24_25/filter_PremierLeague_24_25.csv", index=False) # Export

# Player league average added to current DataFrame
# df_avg = player_league_average_only(df)  # Create league average data set
# df_avg = df_avg.reindex(columns=df.columns)  # align column order
# df_with_avg = pd.concat([df, df_avg], ignore_index=True)  # Combine with original data
# reformat_powerbi(df_with_avg, "output/PremierLeague_24_25/reformat_PremierLeague_24_25.csv")

# Total + per90
# This is a BIG table with both total and per90 --> Comment out this if don't need --> Use PowerBI to calculate per90
# Calculate per90 for current DataFrame
df = calculate_per90(df) # This calculates per90 stats
# df.to_csv("output/PremierLeague_24_25/BIG_per90_PremierLeague_24_25.csv", index=False) # Export


### NOT POSITION BASED

# Calculate league average and append ENTIRE league average to entire list (not position based), then reformat
# df_avg_per90 = player_league_average_only(df) # Create league average data set
# df_avg_per90 = df_avg_per90.reindex(columns=df.columns)  # align column order
# df_with_avg_per90 = pd.concat([df, df_avg_per90], ignore_index=True) # Combine with original data
# reformat_powerbi(df_with_avg_per90, "output/PremierLeague_24_25/final_players_with_league_avg_PremierLeague_24_25.csv")

# SINGLE ROW CSV --> We do this so that every time we need to compare some new averages, we can just take this, and append to our BIG table
# df_avg_per90 = player_league_average_only(df)
# reformat_powerbi(df_avg_per90, "output/PremierLeague_24_25/final_single_row_PremierLeague_24_25.csv")

### NOT POSITION BASED


### POSITION BASED

# Calculate league average based on POSITION
# List for reference: ["DF", "DF, FW", "DF, MF", "FW", "FW, DF", "FW, MF", "GK", "MF", "MF, DF", "MF, FW"]
# df_avg_per90_position = player_league_average_by_position(df, positions=["FW", "FW, MF", "MF", "MF, FW"])
# df_avg_per90_position = df_avg_per90_position.reindex(columns=df.columns)  # align column order
# df_with_avg_per90_position = pd.concat([df, df_avg_per90_position], ignore_index=True)  # Combine with original data
# reformat_powerbi(df_with_avg_per90_position, "output/PremierLeague_24_25/Attackers_final_players_with_league_avg_position_PremierLeague_24_25.csv")

# SINGLE ROW CSV --> We do this so that every time we need to compare some new averages, we can just take this, and append to our BIG table
df_avg_per90_single_row = player_league_average_by_position(df, positions=["FW", "FW, MF", "MF", "MF, FW"])
reformat_powerbi(df_avg_per90_single_row, "output/PremierLeague_24_25/Attackers_final_single_row_PremierLeague_24_25.csv")

### POSITION BASED


reformat_powerbi(df, "output/PremierLeague_24_25/BIG_reformat_PremierLeague_24_25.csv")


print("Pipeline complete ✅")

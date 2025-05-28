from scraping.player_scraper import scrape_player_table

url = "https://fbref.com/en/players/e7fcf289/Florian-Wirtz"
table_ids = [
    "stats_standard_dom_lg", "stats_shooting_dom_lg", "stats_passing_dom_lg",
    "stats_passing_types_dom_lg", "stats_gca_dom_lg", "stats_defense_dom_lg",
    "stats_possession_dom_lg", "stats_playing_time_dom_lg", "stats_misc_dom_lg"
]

dfs = []
for i, table_id in enumerate(table_ids, 1):
    df = scrape_player_table(url, table_id)
    if df is not None:
        print(f"✅ Table {i}: {df.shape} — {table_id}")
        dfs.append(df)
    else:
        print(f"❌ Table {i} not found: {table_id}")

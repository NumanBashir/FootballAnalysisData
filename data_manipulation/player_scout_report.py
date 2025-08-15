import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO


# Filter by minimum stats method
def filter_by_best_rows(df, num):
    df['Percentile'] = pd.to_numeric(df['Percentile'], errors='coerce')
    return df[df['Percentile'] >= num]

def filter_by_worst_rows(df, num):
    df['Percentile'] = pd.to_numeric(df['Percentile'], errors='coerce')
    df['Per 90'] = pd.to_numeric(df['Per 90'], errors='coerce')  # Ensure it's numeric
    return df[(df['Percentile'] <= num) & (df['Per 90'] > 0)]

def filter_top_percentile_stats(df, top_n=5):
    """
    Returns the top `top_n` rows based on the highest Percentile values.

    ⚠️ Note:
    If multiple stats have the same percentile value, only the first `top_n` rows are selected.
    This means some equally high stats could be left out due to ordering — be cautious when interpreting.

    Parameters:
        df (pd.DataFrame): DataFrame with 'Percentile' column
        top_n (int): Number of top rows to return

    Returns:
        pd.DataFrame: Top `top_n` rows by Percentile
    """
    df['Percentile'] = pd.to_numeric(df['Percentile'], errors='coerce')
    df_sorted = df.sort_values(by='Percentile', ascending=False)
    return df_sorted.head(top_n)

# Reformat for PowerBI
def reformat_powerbi(df, path):
    df.to_csv(path, sep=';', decimal=',', index=False)

# Create scraper
scraper = cloudscraper.create_scraper()

# URL of the scouting report
url = "https://fbref.com/en/players/dc62b55d/scout/365_m1/Matheus-Cunha-Scouting-Report"

# Get the response
response = scraper.get(url)

# Parse the HTML directly
soup = BeautifulSoup(response.text, "html.parser")

# Try to find the table directly (not in comments)
table = soup.find('table', {'id': 'scout_full_FW'})

if table:
    df = pd.read_html(StringIO(str(table)))[0]
    df.columns = ['Statistic', 'Per 90', 'Percentile']  # optional rename

    df.dropna(how='all', inplace=True)

    # Drop rows where there is not numbers in Per 90
    df['Per 90'] = pd.to_numeric(df['Per 90'], errors='coerce')  # Non-numeric → NaN
    df = df[df['Per 90'].notna()]  # Keep only numeric rows

    # df = df.drop_duplicates(subset='Statistic', keep='first')
    df = df.drop_duplicates()

    # Use this method if you want to filter by best --> Comment if you want all stats
    # df = filter_top_percentile_stats(df, 5)
    df_best = filter_by_best_rows(df, 98)
    # reformat_powerbi(df_best, "player_scout_reports/percentiles_scouting_report/matheus_cunha/min98_percentile_matheus_cunhaFW.csv")

    df_worst = filter_by_worst_rows(df, 40)
    reformat_powerbi(df_worst, "player_scout_reports/percentiles_scouting_report/matheus_cunha/max40_percentile_matheus_cunhaFW.csv")

    print("✅ Scout report saved as 'min98_percentile_matheus_cunhaFW.csv'")
else:
    print("❌ Table 'scout_full_MF' not found directly in HTML")

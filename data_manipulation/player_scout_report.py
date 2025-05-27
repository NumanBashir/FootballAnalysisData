import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO


# Filter by minimum stats method
def filter_by_best_rows(df, num):
    df['Percentile'] = pd.to_numeric(df['Percentile'], errors='coerce')
    return df[df['Percentile'] >= num]

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

# Create scraper
scraper = cloudscraper.create_scraper()

# URL of the scouting report
url = "https://fbref.com/en/players/0d9b2d31/scout/365_m1/Pedri-Scouting-Report"

# Get the response
response = scraper.get(url)

# Parse the HTML directly
soup = BeautifulSoup(response.text, "html.parser")

# Try to find the table directly (not in comments)
table = soup.find('table', {'id': 'scout_full_MF'})

if table:
    df = pd.read_html(StringIO(str(table)))[0]
    df.columns = ['Statistic', 'Per 90', 'Percentile']  # optional rename

    df.dropna(how='all', inplace=True)

    # Drop rows where there is not numbers in Per 90
    df['Per 90'] = pd.to_numeric(df['Per 90'], errors='coerce')  # Non-numeric → NaN
    df = df[df['Per 90'].notna()]  # Keep only numeric rows

    # Use this method if you want to filter by best --> Comment if you want all stats
    # df = filter_by_best_rows(df, 95)

    df = filter_top_percentile_stats(df, 5)

    df.to_csv("5_scout_report_pedri.csv", index=False)
    print("✅ Scout report saved as '5_scout_report_pedri.csv'")
else:
    print("❌ Table 'scout_full_MF' not found directly in HTML")

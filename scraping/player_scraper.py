from urllib import response
import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def scrape_player_table(url: str, table_id: str):
    """
    Scrapes a visible FBref table directly from a player profile page (not from comments).

    Args:
        url (str): Full URL of the player page.
        table_id (str): The table's HTML ID (e.g. "stats_standard_dom_lg").

    Returns:
        pd.DataFrame or None: Cleaned DataFrame if found and contains 'Season', otherwise None.
    """
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)

    print(f"[DEBUG] Table ID: {table_id}")
    print("Response length:", len(response.text))
    print(response.text[:500])  # first 500 characters of the HTML

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find('table', {'id': table_id})
    if table:
        df = pd.read_html(StringIO(str(table)))[0]
        
        # Fix multiindex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(-1)

        df.dropna(how="all", inplace=True)
        df.reset_index(drop=True, inplace=True)

        if "Season" in df.columns:
            return df

    return None

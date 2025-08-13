import cloudscraper
from bs4 import BeautifulSoup, Comment
import pandas as pd
from io import StringIO

def scrape_team_table(url: str, table_id: str):
    """
    Scrapes a team table from a league stats page.
    Handles both visible HTML tables and tables hidden in comments.
    """
    # scraper = cloudscraper.create_scraper()
    scraper = cloudscraper.create_scraper(
        browser={
            'custom': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/127.0.0.1 Safari/537.36'
        }
    )

    response = scraper.get(url)

    # 🔍 Debug: Check if we got blocked or the page is different
    print(f"[DEBUG] Table ID: {table_id}")
    print("Response length:", len(response.text))
    print(response.text[:500])  # first 500 characters of the HTML

    soup = BeautifulSoup(response.text, "html.parser")

    # 1️⃣ Try finding table directly in the HTML
    table = soup.find("table", {"id": table_id})
    if table:
        df = pd.read_html(StringIO(str(table)))[0]
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(-1)
        df.dropna(how="all", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    # 2️⃣ If not found, look inside HTML comments (rare for teams)
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        if table_id in comment:
            comment_soup = BeautifulSoup(comment, "html.parser")
            table = comment_soup.find("table", {"id": table_id})
            if table:
                df = pd.read_html(StringIO(str(table)))[0]
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(-1)
                df.dropna(how="all", inplace=True)
                df.reset_index(drop=True, inplace=True)
                return df

    # If still nothing
    return None

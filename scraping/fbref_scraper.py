import cloudscraper
from bs4 import BeautifulSoup, Comment
import pandas as pd
from io import StringIO

def scrape_table(url, table_id):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        if table_id in comment:
            comment_soup = BeautifulSoup(comment, "html.parser")
            table = comment_soup.find('table', {'id': table_id})
            if table:
                df = pd.read_html(StringIO(str(table)))[0]
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(-1)
                df = df[~df.apply(lambda row: row.astype(str).str.contains('Player').any(), axis=1)]
                df.reset_index(drop=True, inplace=True)
                return df
    return None

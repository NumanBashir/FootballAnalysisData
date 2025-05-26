import cloudscraper
from bs4 import BeautifulSoup, Comment
import pandas as pd
from io import StringIO

# Create a cloudscraper session
scraper = cloudscraper.create_scraper()

# URL
url = "https://fbref.com/en/comps/20/gca/Bundesliga-Stats"

# Make the request
response = scraper.get(url)

# Parse the HTML using BeautifulSoup which is a library for parsing HTML and XML documents.
soup = BeautifulSoup(response.text, "html.parser")

# Look through HTML comments to find table
table = None
comments = soup.find_all(string=lambda text: isinstance(text, Comment))
for comment in comments:
    if 'stats_gca' in comment:
        comment_soup = BeautifulSoup(comment, "html.parser")
        table = comment_soup.find('table', {'id': 'stats_gca'})
        if table:
            break

# Convert to DataFrame and save also clean the data
if table:
    df = pd.read_html(StringIO(str(table)))[0]
    
    # Removes the header
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(-1)
    
    # Remove any row that contains 'Player' anywhere in the row
    # This is to ensure that we do not have any rows that are not actual player data
    df = df[~df.apply(lambda row: row.astype(str).str.contains('Player').any(), axis=1)]

    # Reset index after dropping rows
    df.reset_index(drop=True, inplace=True)

    df.to_csv("2bundesliga_gca.csv", index=False)
    print("Table saved ✅")
else:
    print("Could not find table ❌")

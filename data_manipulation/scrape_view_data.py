import cloudscraper
from bs4 import BeautifulSoup, Comment
import pandas as pd
from io import StringIO

# Create cloudscraper session to scrape the table
scraper = cloudscraper.create_scraper()

# URL of the table
url = "https://fbref.com/en/comps/20/gca/Bundesliga-Stats"
response = scraper.get(url)

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Look through HTML comments for the table
table = None
comments = soup.find_all(string=lambda text: isinstance(text, Comment))
for comment in comments:
    if 'stats_gca' in comment:
        comment_soup = BeautifulSoup(comment, "html.parser")
        table = comment_soup.find('table', {'id': 'stats_gca'})
        if table:
            break

# Display the table
if table:
    df = pd.read_html(StringIO(str(table)))[0]
    print(df.head(10))  # Show first 10 rows
else:
    print("❌ Table not found.")

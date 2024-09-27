from settings import *
import requests
import pandas as pd
from urllib.parse import quote_plus
from storage import DBStorage
from requests.exceptions import RequestException

def search_api(query, pages=int((RESULT_COUNT/10))):
    results = []
    for i in range(0, pages):
        start = i * 10 + i
        url = SEARCH_URL.format(
            key=SEARCH_KEY,
            cx=SEARCH_ID,
            query=quote_plus(query),
            start=start
        )

        response = requests.get(url)
        data = response.json()

        results += data["items"]

    # Results will be a list of dictionaries
    res_df = pd.DataFrame.from_dict(results)

    # 1-11 for the first page of results
    res_df["rank"] = list(range(1, res_df.shape[0]+1))
    res_df = res_df[["link", "rank", "snippet", "title"]]

    # We only need the above specified fields
    return res_df

# List of links, getting full html from those pages
def scrape_page(links):
    html = []
    for link in links:
        try:
            # Downloads the html of that page, useful for later filtering
            data = requests.get(link, timeout=5)
            # Append text property of data
            html.append(data.text)
        # Occurs when requests cant download the page properly
        except RequestException:
            html.append("")
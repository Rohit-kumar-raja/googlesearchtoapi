import requests
from bs4 import BeautifulSoup
import json


def google_search(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    params = {"q": query, "hl": "en"}

    response = requests.get(
        "https://www.google.com/search", headers=headers, params=params
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for g in soup.find_all("div", class_="tF2Cxc"):
        title = g.find("h3").text if g.find("h3") else "N/A"
        link = g.find("a")["href"] if g.find("a") else "N/A"
        description = (
            g.find("span", class_="aCOpRe").text
            if g.find("span", class_="aCOpRe")
            else "N/A"
        )
        results.append({"title": title, "link": link, "description": description})

    return results


# Replace 'your_search_query' with your actual search query
query = "site:codersmile.com what is php"
results = google_search(query)
print(results)

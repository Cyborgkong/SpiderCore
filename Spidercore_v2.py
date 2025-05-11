# LIST SOURCES
sources = [
    {
        "name": "BBC World",
        "url": "https://www.bbc.com/news/world",
        "selector": {"tag": "h2", "class": "sc-9d830f2a-3 jqQlce"},
    },
    {
        "name": "BBC Technology",
        "url": "https://www.bbc.com/news/technology",
        "selector": {"tag": "h2", "class": "sc-9d830f2a-3 jqQlce"},
    },
    {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com/",
        "selector": {"tag": "a", "class": "titlelink"},
    },
]

# START SCRAPE
import requests
from bs4 import BeautifulSoup


def scrape_headlines(url, selector):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTPError if bad response
    except requests.RequestException as e:
        print(f"[!] Failed to fetch {url} - {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    headlines = soup.find_all(selector["tag"], class_=selector["class"])
    return [h.get_text(strip=True) for h in headlines]


# LOOP THROUGH
all_data = []
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for source in sources:
    print(f"[+] Scraping {source['name']}...")
    headlines = scrape_headlines(source["url"], source["selector"])
    for headline in headlines:
        all_data.append(
            {"source": source["name"], "headline": headline, "timestamp": timestamp}
        )

print(f"[+] Scraped total of {len(all_data)} headlines.")

# SAVE IN CSV FILE
import csv

with open("output/aggregated_headlines.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Source", "Headline", "Timestamp"])

    for item in all_data:
        writer.writerow([item["source"], item["headline"], item["timestamp"]])

print("[+] All headlines saved to output/aggregated_headlines.csv")
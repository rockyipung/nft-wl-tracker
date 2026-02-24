import requests
import os
import feedparser
from datetime import datetime, timezone

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🔥 Fokus utama
BASE_KEYWORD = "free mint"

REGIONS = [
    "USA", "US", "New York", "California", "Texas", "EST", "PST",
    "UK", "France", "Germany", "Spain", "Italy", "Europe", "CET", "GMT"
]

def send_telegram(text):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})


def search_rss(query):
    q = query.replace(" ", "+")
    url = f"https://nitter.net/search/rss?f=tweets&q={q}+lang:en"
    feed = feedparser.parse(url)
    return feed.entries


def is_recent(entry):
    if not hasattr(entry, "published_parsed"):
        return False

    tweet_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    return (now - tweet_time).total_seconds() / 3600 <= 2


def contains_region(text):
    for region in REGIONS:
        if region.lower() in text.lower():
            return True
    return False


def main():
    send_telegram("🚀 FREE MINT GLOBAL HUNTER STARTED")

    results = search_rss(BASE_KEYWORD)

    found = 0

    for entry in results[:10]:

        if is_recent(entry) and contains_region(entry.title):

            link = entry.link
            text = entry.title

            message = f"""🔥 FREE MINT ALERT

Tweet:
{text}

Link:
{link}
"""
            send_telegram(message)
            found += 1

    if found == 0:
        send_telegram("❌ No free mint with region detected.")


if __name__ == "__main__":
    main()

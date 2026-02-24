import requests
import os
import feedparser
from datetime import datetime, timezone

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🔥 Keyword hunter regional
KEYWORDS = [
    "whitelist nft USA",
    "free mint NFT UK",
    "NFT mint Europe",
    "NFT whitelist France",
    "ERC721 mint Germany"
]

def send_telegram(text):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Telegram secret missing")
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

    diff_minutes = (now - tweet_time).total_seconds() / 60

    # 🔥 hanya tweet maksimal 2 jam
    return diff_minutes <= 120


def main():
    send_telegram("🚀 RSS HUNTER US/EU STARTED")

    total_found = 0

    for keyword in KEYWORDS:
        results = search_rss(keyword)

        for entry in results[:5]:
            if is_recent(entry):
                link = entry.link
                text = entry.title

                message = f"""🔥 NFT WL ALERT

Keyword: {keyword}
Tweet: {text}
Link: {link}
"""
                send_telegram(message)
                total_found += 1

    if total_found == 0:
        send_telegram("❌ No fresh US/EU whitelist tweets found.")


if __name__ == "__main__":
    main()

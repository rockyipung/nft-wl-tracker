import requests
import os
import feedparser
from datetime import datetime, timezone

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

KEYWORDS = [
    "whitelist nft USA",
    "free mint NFT UK",
    "NFT mint Europe",
    "NFT whitelist France",
    "ERC721 mint Germany"
]

def send_telegram(text):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(telegram_url, json=payload)

def search_x(query):
    q = query.replace(" ", "+")
    url = f"https://nitter.net/search/rss?f=tweets&q={q}+lang:en"
    return feedparser.parse(url).entries

def is_recent(entry):
    if not hasattr(entry, "published_parsed"):
        return False
    
    tweet_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    diff_minutes = (now - tweet_time).total_seconds() / 60
    
    return diff_minutes <= 120  # max 2 jam

def main():
    send_telegram("🚀 HUNTER MODE US & EUROPE STARTED")

    total_sent = 0

    for keyword in KEYWORDS:
        results = search_x(keyword)

        for entry in results[:5]:
            if is_recent(entry):
                message = f"""🔥 NFT WL ALERT (US/EU)

Keyword: {keyword}
Title: {entry.title}
Link: {entry.link}
"""
                send_telegram(message)
                total_sent += 1

    if total_sent == 0:
        send_telegram("❌ No fresh US/EU NFT whitelist found.")

if __name__ == "__main__":
    main()

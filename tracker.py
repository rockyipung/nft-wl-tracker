import requests
import os
import feedparser
from datetime import datetime, timezone, timedelta

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

KEYWORD = "free mint"

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

    # 🔥 2 HARI = 48 JAM
    return (now - tweet_time) <= timedelta(days=2)


def main():
    send_telegram("🚀 FREE MINT GLOBAL HUNTER STARTED (<2 Days)")

    results = search_rss(KEYWORD)

    found = 0

    for entry in results[:20]:

        if is_recent(entry):

            message = f"""🔥 FREE MINT ALERT

Tweet:
{entry.title}

Link:
{entry.link}
"""

            send_telegram(message)
            found += 1

    if found == 0:
        send_telegram("❌ No free mint tweets found in last 2 days.")

print("TOTAL RSS RESULTS:", len(results))
for e in results[:5]:
    print("RAW TITLE:", e.title)


if __name__ == "__main__":
    main()

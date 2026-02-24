import requests
import os
import feedparser
from datetime import datetime, timezone, timedelta

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Tambahkan kata kunci di sini
KEYWORDS = ["free mint", "wl", "nft"]


def send_telegram(text):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Telegram secret missing")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    # Menambahkan disable_web_page_preview agar link tidak melebarkan chat
    requests.post(url, json={"chat_id": CHAT_ID, "text": text, "disable_web_page_preview": True})


def search_rss(query):
    q = query.replace(" ", "+")
    # Menambahkan filter lang:en agar hasil tetap bahasa inggris
    url = f"https://nitter.net/search/rss?f=tweets&q={q}+lang:en"
    
    try:
        feed = feedparser.parse(url)
        print(f"Searching for: '{query}' | Status: {feed.status if hasattr(feed, 'status') else 'NO STATUS'} | Found: {len(feed.entries)}")
        return feed.entries
    except Exception as e:
        print(f"Error fetching RSS for {query}: {e}")
        return []


def is_recent(entry):
    if not hasattr(entry, 'published_parsed'):
        return False

    tweet_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    return (now - tweet_time) <= timedelta(days=2)


def main():
    print("🚀 HUNTER STARTED...")
    # send_telegram("🚀 MULTI-KEYWORD HUNTER STARTED (Free Mint, WL, NFT)")

    seen_links = set()  # Untuk menyimpan link yang sudah dikirim agar tidak dobel
    total_found = 0

    # Loop untuk setiap kata kunci
    for keyword in KEYWORDS:
        results = search_rss(keyword)

        for entry in results[:20]: # Batasi 20 hasil per keyword untuk hemat kuota

            # Cek apakah link ini sudah pernah dikirim
            if entry.link in seen_links:
                continue

            if is_recent(entry):
                # Menambahkan tag [KEYWORD] agar tahu trigger dari kata apa
                message = f"""🔥 [{keyword.upper()}] ALERT

Tweet:
{entry.title}

Link:
{entry.link}
"""

                send_telegram(message)
                seen_links.add(entry.link)
                total_found += 1

    if total_found == 0:
        print("❌ No relevant tweets found in last 2 days.")
        # send_telegram("❌ No tweets found for keywords: Free Mint, WL, NFT in last 2 days.")
    else:
        print(f"✅ Sent {total_found} unique alerts.")

if __name__ == "__main__":
    main()

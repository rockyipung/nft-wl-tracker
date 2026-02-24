import requests
import os
from datetime import datetime, timezone, timedelta

BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"

QUERY = """
(whitelist OR "free mint" OR "mint live")
(USA OR UK OR France OR Germany OR Europe)
lang:en -is:retweet
"""

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def search_x():
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    
    params = {
        "query": QUERY,
        "max_results": 10,
        "tweet.fields": "created_at,author_id"
    }
    
    response = requests.get(SEARCH_URL, headers=headers, params=params)
    
    if response.status_code != 200:
        print(response.text)
        return []
    
    return response.json().get("data", [])

def is_recent(tweet_time):
    tweet_time = datetime.fromisoformat(tweet_time.replace("Z","+00:00"))
    now = datetime.now(timezone.utc)
    return (now - tweet_time) <= timedelta(hours=2)

def main():
    send_telegram("🚀 HUNTER MODE API X STARTED")

    tweets = search_x()

    found = 0

    for tweet in tweets:
        if is_recent(tweet["created_at"]):
            link = f"https://x.com/i/web/status/{tweet['id']}"
            
            message = f"""🔥 NFT WL ALERT (API X)

Text:
{tweet['text']}

Link:
{link}
"""
            send_telegram(message)
            found += 1

    if found == 0:
        send_telegram("❌ No fresh US/EU NFT whitelist found.")

if __name__ == "__main__":
    main()

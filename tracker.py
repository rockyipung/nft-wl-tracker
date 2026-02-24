import requests
import os
from datetime import datetime, timedelta

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

def search_repos():
    time_filter = (datetime.utcnow() - timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    url = f"https://api.github.com/search/repositories?q=nft+mint+created:>{time_filter}&sort=stars&order=desc"
    
    r = requests.get(url, headers=headers)
    return r.json()

def send_telegram(text):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(telegram_url, json=payload)

def main():
    data = search_repos()
    
    for repo in data.get("items", []):
        if repo["stargazers_count"] > 5 and not repo["fork"]:
            message = f"""
🚀 NFT Repo Detected

Name: {repo['name']}
Stars: {repo['stargazers_count']}
URL: {repo['html_url']}
"""
            send_telegram(message)

if __name__ == "__main__":
    main()

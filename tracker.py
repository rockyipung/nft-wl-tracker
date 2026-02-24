import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SEARCH_KEYWORD = os.getenv("SEARCH_KEYWORD") or "nft"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

def search_repos():
    query = f"{SEARCH_KEYWORD} OR erc721 OR erc1155 whitelist mint"
    url = f"https://api.github.com/search/repositories?q={query}+in:name,description,readme&sort=updated&order=desc&per_page=10"
    
    r = requests.get(url, headers=headers)
    print("GitHub API Status:", r.status_code)
    return r.json()

def send_telegram(text):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("ERROR: TELEGRAM_TOKEN or CHAT_ID is missing")
        return
    
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    r = requests.post(telegram_url, json=payload)
    print("Telegram Status:", r.status_code)
    print("Telegram Response:", r.text)

def main():
    print("Workflow started")
    print("Searching for:", SEARCH_KEYWORD)

    send_telegram(f"🔎 Searching GitHub for: {SEARCH_KEYWORD}")

    data = search_repos()
    
    if "items" not in data:
        print("No items found or API limit reached")
        send_telegram("⚠️ No results found or API limit reached.")
        return

    count = 0

    for repo in data.get("items", []):
        if repo["stargazers_count"] > 3 and not repo["fork"]:
            
            message = f"""🚀 NFT Repo Detected

Name: {repo['name']}
Stars: {repo['stargazers_count']}
Updated: {repo['updated_at']}
URL: {repo['html_url']}
"""
            send_telegram(message)
            count += 1

        if count >= 5:
            break

    if count == 0:
        send_telegram("❌ No strong NFT repo found.")

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import json, sys
from datetime import datetime

# ← Replace these with your own values:
USERNAME       = "dreamyroni"
ZAPIER_WEBHOOK = "https://hooks.zapier.com/hooks/catch/123456/abcdef"

def fetch_followers(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/14.0 Mobile/15A372 Safari/604.1"
        ),
        "Accept-Language": "en-US,en;q=0.9"
    }
    print(f"[DEBUG] GET {url}")
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    html = resp.text

    soup = BeautifulSoup(html, "html.parser")
    meta = soup.find("meta", attrs={"name": "description"})
    if not meta or not meta.get("content"):
        raise ValueError("Could not find meta[name=description] tag")

    content = meta["content"]
    # e.g. "1,234 Followers, 56 Following, 78 Posts – See Instagram photos and videos from ..."
    followers_str = content.split(" Followers")[0]
    count = int(followers_str.replace(",", "").strip())
    print(f"[DEBUG] followers = {count}")
    return count

def main():
    try:
        cnt = fetch_followers(USERNAME)
        payload = {
            "timestamp":  datetime.utcnow().isoformat(),
            "channel":    "instagram",
            "identifier": USERNAME,
            "followers":  cnt
        }
        print(f"[DEBUG] Posting to Zapier: {json.dumps(payload)}")
        r = requests.post(ZAPIER_WEBHOOK, json=payload)
        print(f"[DEBUG] Zapier replied {r.status_code}: {r.text}")
        r.raise_for_status()
    except Exception as e:
        print("[ERROR]", e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

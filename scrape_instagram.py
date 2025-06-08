import requests, json, sys
from datetime import datetime
from bs4 import BeautifulSoup

USERNAME       = "dreamyroni"
ZAPIER_WEBHOOK = "https://hooks.zapier.com/hooks/catch/123456/abcdef"

def fetch_followers(username):
    url  = f"https://www.instagram.com/{username}/"
    print(f"[DEBUG] GET {url}")
    resp = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    resp.raise_for_status()
    soup    = BeautifulSoup(resp.text, "html.parser")
    tag     = soup.find("meta", property="og:description")
    if not tag or not tag.get("content"):
        raise ValueError("Could not find og:description meta")
    content = tag["content"]
    followers_str = content.split(" Followers")[0]
    return int(followers_str.replace(",", "").strip())

def main():
    try:
        cnt = fetch_followers(USERNAME)
        payload = {
            "timestamp":  datetime.utcnow().isoformat(),
            "channel":    "instagram",
            "identifier": USERNAME,
            "followers":  cnt
        }
        print(f"[DEBUG] Posting to Zapier: {payload}")
        r = requests.post(ZAPIER_WEBHOOK, json=payload)
        print(f"[DEBUG] Zapier replied {r.status_code}: {r.text}")
        r.raise_for_status()
    except Exception as e:
        print("[ERROR]", e, file=sys.stderr)
        sys.exit(1)

if __name__=="__main__":
    main()

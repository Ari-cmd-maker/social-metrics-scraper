import requests, re, json, sys
from datetime import datetime

USERNAME       = "dreamyroni"
ZAPIER_WEBHOOK = "https://hooks.zapier.com/hooks/catch/123456/abcdef"

def fetch_followers(username):
    url  = f"https://www.instagram.com/{username}/"
    resp = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    resp.raise_for_status()
    html = resp.text

    # Try to pull the JSON from window.__additionalDataLoaded(...)
    m = re.search(
        r"window\.__additionalDataLoaded\('/" + re.escape(username) + r"/',\s*({.+?})\);",
        html
    )
    if not m:
        raise ValueError("Couldn't extract __additionalDataLoaded JSON")
    data = json.loads(m.group(1))

    # Navigate to the user object
    user = data["graphql"]["user"]
    return user["edge_followed_by"]["count"]

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

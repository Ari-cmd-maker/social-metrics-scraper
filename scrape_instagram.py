import requests, re, json, sys
from datetime import datetime

# ← your values:
USERNAME       = "dreamyroni"
ZAPIER_WEBHOOK = "https://hooks.zapier.com/hooks/catch/23268473/uyu9h40/"

def fetch_followers(username):
    url = f"https://www.instagram.com/{username}/"
    print(f"[DEBUG] GET {url}")
    resp = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    resp.raise_for_status()
    html = resp.text

    # Extract the JSON blob from window._sharedData
    m = re.search(r"window\._sharedData = (.+?);</script>", html)
    if not m:
        raise ValueError("Could not find sharedData JSON in page")
    shared_data = json.loads(m.group(1))

    # Drill into the structure to get follower count
    user = shared_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]
    count = user["edge_followed_by"]["count"]
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
        print(f"[DEBUG] posting to Zapier: {payload}")
        r = requests.post(ZAPIER_WEBHOOK, json=payload)
        print(f"[DEBUG] Zapier responded {r.status_code}: {r.text}")
        r.raise_for_status()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__=="__main__":
    main()

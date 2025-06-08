import requests, json, sys
from datetime import datetime

USERNAME       = "dreamyroni"
ZAPIER_WEBHOOK = "https://hooks.zapier.com/hooks/catch/123456/abcdef"

def fetch_followers(username):
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
                      "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                      "Version/14.0 Mobile/15A372 Safari/604.1",
        "x-ig-app-id": "936619743392459",
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    user = data["data"]["user"]
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

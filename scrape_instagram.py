import requests, json
from datetime import datetime

USERNAME = "dreamyroni"
ZAPIER_WEBHOOK = "https://hooks.zapier.com/hooks/catch/23268473/uyu9h40/"

def fetch_followers(username):
    url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
    data = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}).json()
    cnt = data["graphql"]["user"]["edge_followed_by"]["count"]
    return cnt

def main():
    followers = fetch_followers(USERNAME)
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "channel": "instagram",
        "identifier": USERNAME,
        "followers": followers
    }
    # send to Zapier
    requests.post(ZAPIER_WEBHOOK, json=payload)

if __name__=="__main__":
    main()

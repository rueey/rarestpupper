import os, requests, json
from uuid import uuid4
import urllib
from dog_breeds_classification.src.inference.classify import classify
import math

CLIENT_ID = os.environ["REDDIT_CLIENT_ID"]
CLIENT_SECRET = os.environ["REDDIT_CLIENT_SECRET"]
REDDIT_AUTH_URL = "https://www.reddit.com/api/v1/access_token"
REDDIT_QUERY_URL = "https://www.reddit.com/r/rarepuppers/best/.json?limit=100"
headers = {
    'User-Agent': 'web:rarestpupper:v1 (by /u/cynicalpillow)'
}

'''get_auth_token() requests the reddit api for an authentication token, and returns the
token if it's successful, and returns None otherwise'''

def get_auth_token():
    device_id = str(uuid4())
    d = {"grant_type": "client_credentials", "device_id": device_id}
    r = requests.post(REDDIT_AUTH_URL, headers=headers, params=d, auth=(CLIENT_ID, CLIENT_SECRET))
    parsed_json = json.loads(r.text)
    if "access_token" in parsed_json:
        return parsed_json["access_token"]
    else:
        return None

'''get_hottest_posts(access_token) queries the reddit API for the 100 hottest posts'''

def get_hottest_posts(access_token):
    r = requests.get(REDDIT_QUERY_URL, headers=headers, params={"Authorization": access_token})
    if(r.status_code == 401):
        r = requests.get(REDDIT_QUERY_URL, headers=headers, params={"Authorization": get_auth_token()})
    return json.loads(r.text)

def get_scores_from_parsed_json(parsed_text):
    ret = {}
    for post in parsed_text['data']['children']:
        if(not post['data']['is_video']) and (post['data']['url'].endswith('.jpg') or post['data']['url'].endswith('.png')):
            species = classify('url', post['data']['url'])['breed'].iloc[0]
            score = scoring_algo(post['data']['ups'], post['data']['num_comments'])
            if(species in ret):
                ret[species] = ret[species] + score
            else:
                ret[species] = score
    return ret

def scoring_algo(upvotes, comments):
    return (upvotes//max(comments, 1))+comments

if __name__ == "__main__":
    print(get_scores_from_parsed_json(get_hottest_posts(get_auth_token())))

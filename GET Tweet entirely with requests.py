import sys,os
sys.path.append(os.getcwd())
import requests
import json
import creds


tweet_id = creds.get_id("random tweet")
tweet_id = str(tweet_id)
bearer = creds.get_cred('bearer_token')

headers = {
	'Authorization': 'Bearer {}'.format(bearer)
}

response = requests.request("GET", f"https://api.twitter.com/2/tweets/{tweet_id}", headers=headers, data={})

if response.ok:
	print(json.dumps(json.loads(response.text), indent = 4))
	url = f"https://twitter.com/user/status/{tweet_id}"
	print(f"Link: {url}")

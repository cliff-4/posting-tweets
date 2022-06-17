import sys,os
sys.path.append(os.getcwd())
import requests
import json
import creds

tweet_id = creds.get_id("random tweet")


bearer = creds.get_cred('bearer_token')

headers = {
  'Authorization': 'Bearer {}'.format(bearer)
}

response = requests.request("GET", "https://api.twitter.com/2/tweets/{}".format(str(tweet_id)), headers=headers, data={})

print("OK Response: {}".format(response.ok))
print(json.dumps(json.loads(response.text), indent = 4))

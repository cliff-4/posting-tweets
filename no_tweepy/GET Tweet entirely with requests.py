import requests
import json

url = "https://api.twitter.com/2/tweets/"
tweet_id = str(1228393702244134912)

payload={}

with open("credentials.json", "r") as j:
	creds = json.load(j)

headers = {
  'Authorization': 'Bearer %s' % creds['bearer_token']
}

response = requests.request("GET", (url+tweet_id), headers=headers, data=payload)

print(json.dumps(json.loads(response.text), indent = 4))
print("Response is ok: {}".format(response.ok))

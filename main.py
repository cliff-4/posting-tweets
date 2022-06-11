import tweepy # installed tweepy
import json

def OAuth():
	with open('credentials.json', "r") as j: creds = json.load(j)
	try:
		auth = tweepy.OAuthHandler(creds["api_key"], creds["api_key_secret"])
		auth.set_access_token(creds["access_token"], creds["access_token_secret"])
		return auth
	except Exception as e:
		return None

def tweet_text():
	api = tweepy.API(OAuth())

	text = "suffering"
	#with open('personal/i.txt', "r") as file: text = file.read()
	#with open('personal/i.txt', "w") as file: file.write(str(int(text)+1))
	text = "@siighduuck " + text

	if len(text) > 280: #tweet length fail check
		print("Too long, please shorten the tweet")
		return None
	try: 
		id1 = api.update_status(
			status = text, 
			in_reply_to_status_id = 1535676459808788480, 
			#attachment_url = "https://github.com/cliff-4",
			#possibly_sensitive = False,
			#lat = 46.207684, 
			#long = 6.140700,
			#place_id = "Geneva",
			display_coordinates = True,
			#trim_user = True
		)
		print("tweeted")
	except Exception as e:
		print(e)

def word_thread(word, tweet_id):
	"""
	Takes in a string argument and a tweet ID.
	Then posts a tweet thread with individual letters as thread components.
	Note that two consecutive letters can't be the same.
	"""
	api = tweepy.API(OAuth())

	prev_id = tweet_id
	for i in word:
		text = "@siighduuck " + i
		id1 = api.update_status(
			status = text, 
			in_reply_to_status_id = prev_id
		)
		prev_id = id1.id

if __name__ == "__main__":
	with open("personal/tweet_ids.json", "r") as t: ids = json.load(t)
	#text = input()
	#tweet_text()
	word_thread("STRING", ids["dump_thread"])
	print("Success")
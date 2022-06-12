import tweepy # installed tweepy
import json
import time

with open('credentials.json', "r") as j: creds = json.load(j)
with open("personal/tweet_ids.json", "r") as t: ids = json.load(t)

def OAuth():
	try:
		auth = tweepy.OAuthHandler(creds["api_key"], creds["api_key_secret"])
		auth.set_access_token(creds["access_token"], creds["access_token_secret"])
		return auth
	except Exception as e:
		return None

def tweet_text():

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

	prev_id = tweet_id
	for i in word:
		text = "@siighduuck " + i
		id1 = api.update_status(
			status = text, 
			in_reply_to_status_id = prev_id
		)
		prev_id = id1.id

def create_and_delete():
	"""Creates a tweet and deletes it 60 seconds later."""
	id = api.update_status("Hello there! This will be delete in 60 seconds")
	for i in range(60):
		print("T-", 60-i, " seconds.", end="\r")
		time.sleep(1)
	api.destroy_status(id.id)

def posting_file(ids):
	api.update_status(
		status = "https://github.com/cliff-4/posting-tweets",
		in_reply_to_status_id = ids["Hello World"]
	)

def make_text_commentable(text):
	user_id = ids["self_id"]
	username = api.get_user(user_id = ids["self_id"]).screen_name
	
	return ("@" + username + " " + text)

def media_tweet():
	in_reply_to_id = ids["Hello World"]

	status_text = "GIF!"
	file_address = "personal/kpop dance.gif"

	api.update_status_with_media(
		status = status_text,
		filename = file_address,
		in_reply_to_status_id = in_reply_to_id
	)

if __name__ == "__main__":
	api = tweepy.API(OAuth()) #authenticating. always keep this here.
	
	#tweet_text()
	#word_thread("STRING", ids["dump_thread"])
	#create_and_delete()
	#posting_file(ids)
	#media_tweet()
	
	print("Success")
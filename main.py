# installed tweepy
from ast import Return
from datetime import datetime
import tweepy
import json
import time

with open('credentials.json', "r") as j: creds = json.load(j)

def OAuth():
	try:
		auth = tweepy.OAuthHandler(creds["api_key"], creds["api_key_secret"])
		auth.set_access_token(creds["access_token"], creds["access_token_secret"])
		return auth
	except Exception as e:
		return None

def tweet_text():
	api = tweepy.API(OAuth())

	text = ""
	#with open('personal/i.txt', "r") as file: text = file.read()
	#with open('personal/i.txt', "w") as file: file.write(str(int(text)+1))
	#text = "@siighduuck " + text
	text = "@siighduuck " + "Dump thread"

	if len(text) > 280: #tweet length fail check
		print("Too long, please shorten the tweet")
		return None
	id1 = 0
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
	print(id1.id)

def fun_lol():
	api = tweepy.API(OAuth())
	lenny = "FUCKOFf"

	prev_id = 1535676459808788480
	for i in lenny:
		text = "@siighduuck " + i
		id1 = api.update_status(
			status = text, 
			in_reply_to_status_id = prev_id
		)
		prev_id = id1.id


if __name__ == "__main__":
	#text = input()
	#tweet_text()
	#fun_lol()
	print("Success")
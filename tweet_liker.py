#!/usr/bin/python3
import sys, os
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path) # to make it so this file works when executed from any directory
sys.path.append(os.getcwd()) # so the program can import creds.py
from apscheduler.schedulers.blocking import BlockingScheduler
from creds import * 
import requests
import time
import datetime 
from requests_oauthlib import OAuth1
import json


def auth():
	class authdetails():
		def __init__(self):
			details = get_json("credentials.json")
			self.bearer = details['bearer_token']
			self.api_key = details["api_key"]
			self.api_secret = details["api_key_secret"]
			self.token = details["access_token"]
			self.token_secret = details["access_token_secret"]
	return authdetails()

def main(hours=0, minutes=15, seconds=0):
	time_of_start = datetime.datetime.now()
	strings_to_print = [f"New iteration started at [{time_of_start.strftime('%d-%m-%Y %H:%M:%S')}]"]
	print(*strings_to_print, end = '\r')
	now = time.time()
	
	users = classify("personal/perma_like_list.json")
	
	total_tweets_liked = 0

	total = len(users)
	iter = 0
	strings_to_print.append("")
	for user in users:
		strings_to_print[1] = loading(iter, total, True)
		print(*strings_to_print, end='\r')
		n = 5 # n min = 5 max = 100
		url = f"https://api.twitter.com/2/users/{user.id}/tweets?max_results={n}&tweet.fields=in_reply_to_user_id&exclude=retweets,replies"

		authorization_header = {'Authorization': f'Bearer {credentials.bearer}'}
		response = requests.request("GET", url, headers=authorization_header).json()

		if response['meta']['result_count'] == 0: continue

		try:
			for tweet in response['data']:
				if not ('in_reply_to_user_id' in tweet): break
			is_liked = like(user, tweet["id"], verf_logging = False, nverf_logging = False)
			if is_liked: total_tweets_liked+=1
		except Exception as e:
			print(f"\nUnexpected Error occured for the following user: \n{user.info()}")
			print(f"User Request Response: {response}")
			print(f"Error Message: {e}")
			sys.exit()

		iter += 1
		print(*strings_to_print, end='\r')
	strings_to_print.pop()

	timetaken = time.time() - now
	strings_to_print.append(f"[Time taken: {round(timetaken)} seconds]")
	strings_to_print.append(f"[Tweets liked: {total_tweets_liked} (among {total} users)]")
	print(*strings_to_print)

	next_iter_start = time_of_start + datetime.timedelta(minutes=minutes)
	print(f"Waiting for next session to start... (ETA: {next_iter_start.strftime('%d-%m-%Y %H:%M:%S')})", end='\r')

def scheduled_liking(hours=0, minutes=15, seconds=0): # Default duration between executions = 15 minutes
	scheduler = BlockingScheduler()
	print("\nTwitter API started...")
	scheduler.add_job(main, 'interval', hours=hours, minutes=minutes, seconds=seconds, max_instances=1)
	main()
	try: 
		scheduler.start()
	except KeyboardInterrupt:
		print("\nSuccessfully ended.")

def liking_message_log(screen_name, tweet_id):
	print("\nJust liked this Tweet by @{}: ".format(screen_name), end = "")
	print("https://twitter.com/{}/status/{} at ".format(screen_name, tweet_id), end="")
	print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

def classify(filename):
	people = get_json(filename)
	class twitter_users():

		def __init__(self, username, id, verified):
			self.username = username
			self.id = id
			self.verified = verified
		
		def info(self):
			return f"username: {self.username}\nid: {self.id}\nverified: {self.verified}"
		
	return [twitter_users(key, people[key]['id'], people[key]['verified']) for key in people.keys()]

def like(user, tweet_id_str, verf_logging = False, nverf_logging = True):
	me_id = get_id("self_id")

	# url
	url = f"https://api.twitter.com/2/users/{me_id}/likes"

	# auth
	api_key = credentials.api_key
	api_secret = credentials.api_secret
	token = credentials.token
	token_secret = credentials.token_secret
	authentication = OAuth1(api_key, api_secret, token, token_secret)

	# payload
	payload = json.dumps({"tweet_id": tweet_id_str})

	# headers
	headers = {'Content-Type': 'application/json'}

	# combining it all
	response = requests.post(url, auth=authentication, data=payload, headers=headers).json()

	is_liked = (response['data']['liked'] if "liked" in response['data'] else False) if "data" in response else False

	if is_liked and ((verf_logging and user.verified) or (nverf_logging and not user.verified)):
		# liking_message_log(user.username, tweet_id_str)
		pass
	return is_liked

def loading(progress, base, show_percentage):
	block_str = '█'
	empty_str = '_'
	length = 15

	a = round((progress/base)*length)
	b = length - a
	percent = round(progress/base*100)

	return a*block_str + b*empty_str + (f" {percent}%" if show_percentage else "")

if __name__ == "__main__":
	credentials = auth()
	scheduled_liking()

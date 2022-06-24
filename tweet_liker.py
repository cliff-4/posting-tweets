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
	now = time.time()

	strings_to_print = [f"New iteration started at [{time_of_start.strftime('%d-%m-%Y %H:%M:%S')}]"]
	print(*strings_to_print, end = '\r')

	users = classify("personal/perma_like_list.json")

	# for logging purposes
	## list full of html in string format
	log_list = ['<meta name="twitter:widgets:theme" content="dark">'] 
	
	# importing liked list
	liked_list = get_json("liked_log/already_liked.json")
	
	# loading bar & diagnostics of session
	loading_iter = 0
	total = loading_total = len(users)
	total_tweets_liked = 0
	
	strings_to_print.append("")
	for user in users:
		strings_to_print[1] = loading(loading_iter, loading_total, show_percentage=True)
		print(*strings_to_print, end='\r')
		loading_iter += 1

		# n min = 5 max = 100
		n = 5 

		url = f"https://api.twitter.com/2/users/{user.id}/tweets?max_results={n}&tweet.fields=in_reply_to_user_id&exclude=retweets,replies"

		authorization_header = {'Authorization': f'Bearer {credentials.bearer}'}
		try: 
			response = requests.request("GET", url, headers=authorization_header, timeout=10).json()
		except TimeoutError:
			total -= 1
			continue

		if response['meta']['result_count'] == 0:
			total -= 1
			continue

		for tweet in response['data']:
			if not ('in_reply_to_user_id' in tweet): break
		if (tweet["id"] in liked_list):
			total -= 1
			continue
		else:
			liked_list.append(tweet["id"])

		try:
			is_liked = like(user, tweet["id"], verf_logging = False, nverf_logging = False)
		except Exception as e:
			print(f"\nUnexpected Error occured for the following user- \n{user.info()}")
			print(f"User Request Response: {response}\n\n")
			print(f"Error Message: {e}")
			sys.exit()
		if is_liked: 
			total_tweets_liked+=1
			embed_code = requests.get(f"https://publish.twitter.com/oembed?url=https%3A%2F%2Ftwitter.com%2Fuser%2Fstatus%2F{tweet['id']}")
			toappend = embed_code.json()["html"].split("\n")
			log_list.append(toappend[0])
		else: 
			total -= 1
			continue

		print(*strings_to_print, end='\r')
	strings_to_print.pop()

	# logging
	log_list.append('<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')
	if len(log_list) > 2:
		with open(f"liked_log/{time_of_start.strftime('%Y-%m-%d %H-%M-%S')}.html", "a") as L:
			for tweet_embed in log_list:
				line = tweet_embed + "\n"
				clean_line = line.encode('ascii', 'namereplace').decode()
				L.write(clean_line)

	# exporting liked list
	with open("liked_log/already_liked.json", "w") as J: json.dump(liked_list, J)

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
	try: 
		response = requests.post(url, auth=authentication, data=payload, headers=headers, timeout=10).json()
	except TimeoutError:
		return None
	# If response is taking too long to return, just return NULL and return in the main function as well
	# printing Error message and moving on to waiting for the next instance of schedule.


	is_liked = (response['data']['liked'] if "liked" in response['data'] else False) if "data" in response else False

	if is_liked and ((verf_logging and user.verified) or (nverf_logging and not user.verified)):
		# liking_message_log(user.username, tweet_id_str)
		pass
	return is_liked

def loading(progress, base, show_percentage=True):
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

### Issues
# When skipping tweets based on the list of ids that are already liked, 
# it just simply skips the user and doesn't get to the next possible id in the list 
# which might still be unliked.
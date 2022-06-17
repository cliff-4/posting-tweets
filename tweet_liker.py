import tweepy # installed tweepy
import csv # to get list of people to like
from apscheduler.schedulers.blocking import BlockingScheduler # to schedule perma liking
import datetime # to print when the tweet was liked
import os # for the below commands
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path) # to make it so this file works when executed from any directory
from creds import get_cred, get_id # to get the credentials and ids

def OAuth():
	try:
		auth = tweepy.OAuthHandler(get_cred("api_key"), get_cred("api_key_secret"))
		auth.set_access_token(get_cred("access_token"), get_cred("access_token_secret"))
		return auth
	except Exception as e:
		return None

def main():
	filename = "personal/perma_like_list.csv"
	perma_like_list = []
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		next(csvreader) # to remove the field name
		for row in csvreader: perma_like_list.append(row[0])
	for user in perma_like_list:
		verf = api.get_user(screen_name = user).verified
		count = 2 + verf*3 # Liking past 2 tweets if the user is not verified and past 5 if it is. (This measure is taken in order to neet seem creepy by your friends and relatives. Unless your relative is Elon Musk)
		tweet_object = api.user_timeline(
			screen_name = user,
			count=count,
			since_id = get_id("first tweet of {}".format(str(datetime.datetime.now().year)))
		)
		for tweet in tweet_object:
			try: 
				api.create_favorite(tweet.id)
			except Exception as e:
				continue
			liking_message_log(user, tweet.id)

def liking_message_log(screen_name, tweet_id):
	print("Just liked this Tweet by @{}: ".format(screen_name), end = "")
	print("https://twitter.com/{}/status/{} at ".format(screen_name, tweet_id), end="")
	print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

def scheduled_liking(*kwargs, hours=0, minutes=0, seconds=0):
	scheduler = BlockingScheduler()
	print("Twitter API started...")
	scheduler.add_job(main, 'interval', hours=hours, minutes=minutes, seconds=seconds, max_instances=2)
	main()
	try: 
		scheduler.start()
	except KeyboardInterrupt:
		print("Successfully ended.")


if __name__ == "__main__":
	api = tweepy.API(OAuth())
	scheduled_liking(minutes = 5)
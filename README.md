# posting-tweets

Making this to post tweets automatically at specific times.<br>
Maybe can be used as a template for future fun applications on twitter, like [monitoring eels and tweeting whenever they :zap:ZAP:zap:](https://twitter.com/EelectricMiguel), or [just a tweet liker](https://github.com/cliff-4/posting-tweets/blob/main/tweet_liker.py)

# Setup!
## Install some Dependencies
Get [tweepy (async package not required)](https://docs.tweepy.org/en/stable/install.html)...
```
pip install tweepy
```
...and [apscheduler](https://apscheduler.readthedocs.io/en/3.x/userguide.html)
```
pip install apscheduler
```
## Edit some files
1. `credentials.json`: This file needs to be edited and populated with appropriate credentials according to your application
2. `personal/tweet_ids.json`: add any tweet id you want to use in the program. Any of these can be easily retreived inside the code using functions in `creds.py`. <br>
(P.S. you can use [`API.get_user()`](https://docs.tweepy.org/en/stable/api.html#tweepy.API.get_user) to get your `user_id` if using code that utilizes `tweepy`)
3. `personal/perma_like_list.csv`: `\n` separated list of all user names you wish to follow in `tweet_liker.py`.

## Some links I found very useful
- [Twitter Developer Portal.](https://developer.twitter.com/en/portal/dashboard) (Twitter) <br>
- [Twitter API v2 documentation](https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/introduction) (Twitter) <br>
- [Tweepy API (tweet) documentation.](https://docs.tweepy.org/en/stable/api.html) (Tweepy) <br>
- [User object documentation.](https://www.geeksforgeeks.org/python-user-object-in-tweepy/) (geeksforgeeks) <br>
- [Status object (tweet) documentation.](https://www.geeksforgeeks.org/python-status-object-in-tweepy) (geeksforgeeks) <br>


## You're set!
Using tweepy has been a MASSIVE relief because twitter somehow manages to make POSTMAN generated code almost unusable unless you have in-depth knowledge of the REST API and its proper usage. <br>
Which I don't. <br>
So I use tweepy. <br>
pls don't attack me ;-;
import tweepy
import time
import configparser
import requests
import json
import pytz
import datetime

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Twitter API credentials
consumer_key = config['twitter']['consumer_key']
consumer_secret = config['twitter']['consumer_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# Slack webhook URL and channel
slack_webhook_url = config['slack']['webhook_url']
slack_channel = config['slack']['channel']

# Define the search query
search_query = "Tendermint"
last_tweet_id = None

# Define the timezone to use for the current time
timezone = pytz.timezone('Europe/London')

# Authenticate with the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define the function to search for tweets and send a Slack message
def search_tweets_and_send_slack_message():
    print("The bot is now activated")
    
    global last_tweet_id
    # Search for recent tweets with the search query
    if last_tweet_id is not None:
        tweets = api.search_tweets(q=search_query, count=100, result_type="recent", since_id=last_tweet_id)
    else:
        tweets = api.search_tweets(q=search_query, count=100, result_type="recent")
    for tweet in tweets:
        # Check the number of followers of the user who tweeted
        if tweet.user.followers_count < 100:
            print(f"Skipping tweet with ID {tweet.id} because user has less than 100 followers")
        continue

        # Print the text of the tweet and the URL to the tweet
        tweet_text = tweet.text
        tweet_url = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
        tweet_created_at = tweet.created_at.replace(tzinfo=pytz.UTC).astimezone(timezone)
        if tweet_created_at >= timezone.localize(datetime.datetime.now()) - datetime.timedelta(minutes=15):
            print(f"Found a tweet that mentions {search_query} at {datetime.datetime.now()}:")
            print(tweet_text)
            print(tweet_url)
            if last_tweet_id is None or tweet.id > last_tweet_id:
                last_tweet_id = tweet.id
            # Send a Slack message
            slack_message = {
                "channel": slack_channel,
                "text": f"A tweet that mentions {search_query} was found:\n{tweet_text}\n{tweet_url}"
            }
            response = requests.post(slack_webhook_url, data=json.dumps(slack_message), headers={"Content-Type": "application/json"})
            if response.status_code != 200:
                print(f"Failed to send Slack message: {response.text}")

# Run the search function every 15 minutes
while True:
    try:
        api.verify_credentials()
        print("Authentication OK")
    except Exception as e:
        print("Error during authentication")
        print(e)
    search_tweets_and_send_slack_message()
    time.sleep(900)


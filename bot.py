import tweepy
import time
import config
import datetime

# Twitter API credentials
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except Exception as e:
    print("Error during authentication")
    print(e)

# Define the search query
search_query = "Tendermint"
last_tweet_id = None

# Define the function to search for tweets
def search_tweets():
    global last_tweet_id
    # Search for recent tweets with the search query
    if last_tweet_id is not None:
        tweets = api.search_tweets(q=search_query, count=100, result_type="recent", max_id=last_tweet_id)
    else:
        tweets = api.search_tweets(q=search_query, count=100, result_type="recent")
    for tweet in tweets:
        # Print the text of the tweet and the URL to the tweet
        tweet_text = tweet.text
        tweet_url = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
        print(f"Found a tweet that mentions {search_query} at {datetime.datetime.now()}:")
        print(tweet_text)
        print(tweet_url)
        if last_tweet_id is None or tweet.id < last_tweet_id:
            last_tweet_id = tweet.id

# Run the search function every 15 minutes
while True:
    search_tweets()
    time.sleep(900)
    print("The bot is now on snooze")

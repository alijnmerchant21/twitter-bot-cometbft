import random
import tweepy
import time
import config

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

# Define the reply message and a list of random quotes
reply_message = "Tendermint has been replaced by CometBFT. "
random_quotes = [
    "The universe is a pretty big place. If it's just us, seems like an awful waste of space. - Carl Sagan",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "The greatest glory in living lies not in never falling, but in rising every time we fall. - Nelson Mandela",
    "Be the change that you wish to see in the world. - Mahatma Gandhi",
    "I have not failed. I've just found 10,000 ways that won't work. - Thomas Edison"
]

# Define the function to search for and reply to tweets
def search_and_reply():
    # Search for recent tweets with the search query
    tweets = api.search_tweets(q=search_query, count=1, result_type="recent")
    for tweet in tweets:
        # Check if the tweet has already been replied to
        if tweet.in_reply_to_status_id is not None:
            continue
        # Reply to the tweet
        reply_text = reply_message + random_quotes[random.randint(0, len(random_quotes)-1)]
        api.update_status(
            status=reply_text,
            in_reply_to_status_id=tweet.id,
            auto_populate_reply_metadata=True
        )

# Run the search and reply function every 30 minutes
while True:
    search_and_reply()
    time.sleep(100)

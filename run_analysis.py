import os
from configparser import ConfigParser
import logging
import asyncio
import time
from datetime import datetime

from twikit import Client
import pandas as pd
from random import randint
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Query and constants
X_QUERY = '"scram440" (Royal Enfield OR RC) until:2025-01-28 since:2024-12-02'
MINIMUM_TWEETS = 1000000
COOKIE_FILE = 'x_cookies.json'
TWEETS_DATA_PATH = 'tweets'

# Initialize Twikit client
client = Client('en-US')

# Logger setup
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


async def authenticate_client(username, email, password):
    """Authenticate using cookies or credentials."""
    try:
        if os.path.exists(COOKIE_FILE):
            client.load_cookies(COOKIE_FILE)
            logger.info("Loaded cookies successfully")
        else:
            logger.info("No existing cookies found, performing fresh login...")
            await client.login(auth_info_1=username, auth_info_2=email, password=password)
            client.save_cookies(COOKIE_FILE)
            logger.info("Login successful and cookies saved")
        await client.login(auth_info_1=username, auth_info_2=email, password=password)
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        raise


async def fetch_tweets(tweets) -> list:
    """Fetch tweets using the Twikit client."""
    if tweets is None:
        tweets = await client.search_tweet(query=X_QUERY, product = "Latest", count=100)
    else:
        wait_ts = randint(5, 10)
        logger.info(f'Getting next tweets after {wait_ts} seconds...')
        time.sleep(wait_ts)
        tweets = tweets.next()
    return [
            {
                'created_at': tweet.created_at,
                'text': tweet.text,
                'text_clean': clean_tweet(tweet.text),
                'username': tweet.user.screen_name,
                'retweets': tweet.retweet_count,
                'likes': tweet.favorite_count,
            }
            for tweet in tweets
        ]

def clean_tweet(tweet: str) -> str:
    """Clean tweet text by removing special characters and URLs"""
    return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analyze_sentiment(text: str) -> str:
    """Enhanced sentiment analysis with threshold adjustments"""
    tweet = clean_tweet(text)
    analysis = TextBlob(tweet)
    polarity = analysis.sentiment.polarity
    logger.debug(f'polarity = {polarity}')
    if polarity > 0.2:
        return 'positive'
    elif polarity < -0.2:
        return 'negative'
    else:
        return 'neutral'

async def main():
    """Main function to fetch tweets."""
    # Load credentials from config
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    password = config['X']['password']
    email = config['X']['email']

    # Authenticate the client
    try:
        await authenticate_client(username, email, password)
    except Exception as e:
        logger.error(f"Failed to authenticate: {str(e)}")
        return

    # Fetch tweets
    logger.info("Start fetching tweets")
    tweet_count = 0
    tweets = None

    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await fetch_tweets(tweets)
        except Exception as e:
            logger.info(e)

        if not tweets:
            logger.info("No tweets fetched")
            break

        for tweet in tweets:
            tweet_count += 1            
            logger.debug(tweet)
        
        logger.info(f'Got {tweet_count} tweets')
        
        # Create a DataFrame and analyze sentiment
        df = pd.DataFrame(tweets)
        df['sentiment'] = df['text'].apply(analyze_sentiment)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        df.to_csv(f'{TWEETS_DATA_PATH}/tweets_{timestamp}.csv', index=False)
        logger.info(f'{tweet_count} tweets fetched')


    logger.info(f'Total {tweet_count} tweets fetched')   
  
def get_insights(df: pd.DataFrame):
    """Get the insights to generate sentiment report."""
    print(f"\nSentiment Distribution :")
    print("=" * 25)
    print(df['sentiment'].value_counts(normalize=True).mul(100).round(1))
    
# Run the main function
if __name__ == "__main__":
    asyncio.run(main())

    dfs = [pd.read_csv(os.path.join(TWEETS_DATA_PATH, file)) for file in os.listdir(TWEETS_DATA_PATH)]
    df = pd.concat(dfs, ignore_index=True)
    if df.empty:
        logger.info("No tweets fetched") 
    else:
        get_insights(df)


    
    

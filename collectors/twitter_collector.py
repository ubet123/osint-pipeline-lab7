import tweepy
import os
import time
import random
from dotenv import load_dotenv

load_dotenv()
TWITTER_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

def fetch_twitter(query="OSINT", count=10):  # Minimum is 10 for Twitter v2 API
    """Safe Twitter fetch with proper limits"""
    try:
        time.sleep(random.uniform(5, 8))  # Longer delay for Twitter
        
        client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
        
        # Twitter v2 API requires min 10, max 100 results
        tweets = client.search_recent_tweets(
            query=query,
            max_results=max(min(count, 100), 10),  # Ensure between 10-100
            tweet_fields=["created_at", "author_id", "text"]
        )
        
        results = []
        if tweets and tweets.data:
            for tweet in tweets.data:
                results.append({
                    "platform": "twitter",
                    "user": str(tweet.author_id),
                    "timestamp": str(tweet.created_at),
                    "text": tweet.text,
                    "url": f"https://twitter.com/i/web/status/{tweet.id}"
                })
        
        print(f"Twitter: Collected {len(results)} tweets for '{query}'")
        return results
        
    except tweepy.TooManyRequests:
        print("Twitter rate limit hit. Skipping Twitter for now.")
        return []
    except Exception as e:
        print(f"Twitter error: {e}")
        return []
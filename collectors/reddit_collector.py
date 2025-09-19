import praw
import os
import time
import random
from dotenv import load_dotenv

load_dotenv()
REDDIT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

reddit = praw.Reddit(
    client_id=REDDIT_ID,
    client_secret=REDDIT_SECRET,
    user_agent="osint_lab_app"
)

def fetch_reddit(subreddit="technology", limit=10):
    """Safe Reddit fetch with limited requests"""
    try:
        time.sleep(random.uniform(2, 4))  # Delay before request
        
        results = []
        for post in reddit.subreddit(subreddit).hot(limit=min(limit, 10)):
            results.append({
                "platform": "reddit",
                "user": str(post.author),
                "timestamp": str(post.created_utc),
                "text": post.title + " " + (post.selftext[:200] if post.selftext else ""),
                "url": f"https://reddit.com{post.permalink}"
            })
        
        print(f"Reddit: Collected {len(results)} posts from r/{subreddit}")
        return results
        
    except Exception as e:
        print(f"Reddit error: {e}")
        return []
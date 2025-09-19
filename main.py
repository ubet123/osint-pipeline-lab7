from collectors.twitter_collector import fetch_twitter
from collectors.reddit_collector import fetch_reddit
from collectors.instagram_collector import fetch_instagram
from collectors.github_collector import fetch_github

from utils.cleaner import clean_text, filter_english
from utils.database import save_to_db
from utils.sentiment import add_sentiment

import schedule
import time


def run_pipeline():
    # Collect - Increased limits to get 100+ records
    data = []
    
    # Twitter - multiple queries to get diverse data
    data.extend(fetch_twitter("OSINT", 25))               # 25 tweets
    data.extend(fetch_twitter("cybersecurity", 15))       # 15 tweets  
    data.extend(fetch_twitter("AI", 10))                  # 10 tweets
    
    # Reddit - multiple subreddits
    data.extend(fetch_reddit("technology", 20))           # 20 reddit posts
    data.extend(fetch_reddit("programming", 15))          # 15 reddit posts
    data.extend(fetch_reddit("netsec", 10))               # 10 reddit posts
    
    # Instagram - multiple accounts
    data.extend(fetch_instagram("nasa", 8))               # 8 instagram posts
    data.extend(fetch_instagram("bbcnews", 7))            # 7 instagram posts
    data.extend(fetch_instagram("natgeo", 5))             # 5 instagram posts
    
    # GitHub - multiple search queries
    data.extend(fetch_github("security", 10))             # 10 github repos
    data.extend(fetch_github("data analysis", 8))         # 8 github repos
    data.extend(fetch_github("python", 7))                # 7 github repos

    # Clean
    for d in data:
        d["text"] = clean_text(d["text"])
    data = filter_english(data)

    # Enrich
    data = add_sentiment(data)

    # Store
    save_to_db(data)

    print(f"Collected and stored {len(data)} OSINT records.")
    print(f"Total records now: {get_total_records_count()}")


def get_total_records_count():
    """Helper function to count total records in database"""
    import sqlite3
    conn = sqlite3.connect("data/osint.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM osint_data")
    count = cur.fetchone()[0]
    conn.close()
    return count


def automated_pipeline():
    """Function for scheduled runs"""
    print(f"\n=== Running automated pipeline at {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
    run_pipeline()


if __name__ == "__main__":
    # Run immediately
    run_pipeline()
    
    # Then schedule to run every 2 hours to accumulate more data
    print("\nScheduling pipeline to run every 2 hours...")
    schedule.every(2).hours.do(automated_pipeline)
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)
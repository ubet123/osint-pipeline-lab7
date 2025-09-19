# main_no_instagram.py
from collectors.twitter_collector import fetch_twitter
from collectors.reddit_collector import fetch_reddit
from collectors.github_collector import fetch_github
from utils.cleaner import clean_text, filter_english
from utils.database import save_to_db
from utils.sentiment import add_sentiment

import schedule
import time


def run_pipeline():
    # Collect - NO INSTAGRAM AT ALL
    data = []
    
    # Twitter - multiple queries
    print("Collecting Twitter data...")
    data.extend(fetch_twitter("OSINT", 20))
    data.extend(fetch_twitter("cybersecurity", 15))
    data.extend(fetch_twitter("AI", 10))
    
    # Reddit - multiple subreddits
    print("Collecting Reddit data...")
    data.extend(fetch_reddit("technology", 15))
    data.extend(fetch_reddit("programming", 10))
    data.extend(fetch_reddit("netsec", 5))
    
    # GitHub - multiple search queries
    print("Collecting GitHub data...")
    data.extend(fetch_github("security", 10))
    data.extend(fetch_github("python", 5))
    data.extend(fetch_github("data analysis", 5))

    print(f"Collected {len(data)} raw records")

    # Clean
    for d in data:
        d["text"] = clean_text(d["text"])
    data = filter_english(data)
    print(f"After cleaning: {len(data)} records")

    # Enrich
    data = add_sentiment(data)

    # Store
    save_to_db(data)

    print(f"Stored {len(data)} OSINT records.")
    print(f"Total records in database: {get_total_records_count()}")


def get_total_records_count():
    """Helper function to count total records in database"""
    import sqlite3
    conn = sqlite3.connect("data/osint.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM osint_data")
    count = cur.fetchone()[0]
    conn.close()
    return count


if __name__ == "__main__":
    # Run immediately
    run_pipeline()
    
    # Optional: Run a few more times quickly to get to 100+ records
    for i in range(2):
        time.sleep(2)  # Short delay between runs
        run_pipeline()
    
    print("\n✅ Pipeline completed successfully!")
    print("Run 'python view_data.py' to check your records")
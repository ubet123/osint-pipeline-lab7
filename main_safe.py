from collectors.twitter_collector import fetch_twitter
from collectors.reddit_collector import fetch_reddit
from collectors.github_collector import fetch_github
from utils.cleaner import clean_text, filter_english
from utils.database import save_to_db, get_total_records_count
from utils.sentiment import add_sentiment

import time
import random

def safe_pipeline():
    """Safe pipeline focusing on Reddit and GitHub"""
    print("🚀 Starting safe OSINT collection...")
    data = []
    
    # Phase 1: Reddit (most reliable)
    print("\n📝 Phase 1: Collecting Reddit data...")
    data.extend(fetch_reddit("technology", 12))
    time.sleep(random.uniform(3, 5))
    data.extend(fetch_reddit("programming", 10))
    time.sleep(random.uniform(3, 5))
    data.extend(fetch_reddit("cybersecurity", 8))
    time.sleep(random.uniform(3, 5))
    data.extend(fetch_reddit("datascience", 8))
    
    # Phase 2: GitHub (reliable)
    print("\n🐙 Phase 2: Collecting GitHub data...")
    time.sleep(random.uniform(4, 6))
    data.extend(fetch_github("security", 10))
    time.sleep(random.uniform(3, 5))
    data.extend(fetch_github("python", 8))
    time.sleep(random.uniform(3, 5))
    data.extend(fetch_github("data", 6))
    time.sleep(random.uniform(3, 5))
    data.extend(fetch_github("machinelearning", 6))
    
    # Phase 3: Twitter (optional - skip if problematic)
    print("\n🐦 Phase 3: Collecting Twitter data (optional)...")
    try:
        time.sleep(random.uniform(8, 12))
        twitter_data = fetch_twitter("OSINT", 10)
        if twitter_data:
            data.extend(twitter_data)
    except:
        print("Skipping Twitter due to issues")
    
    print(f"\n📊 Raw collection: {len(data)} records")
    
    # Clean
    for d in data:
        d["text"] = clean_text(d["text"])
    data = filter_english(data)
    print(f"After cleaning: {len(data)} records")
    
    # Skip if no data
    if not data:
        print("❌ No data collected - skipping processing")
        return 0
    
    # Enrich
    data = add_sentiment(data)
    
    # Store
    save_to_db(data)
    
    total_count = get_total_records_count()
    print(f"💾 Stored {len(data)} records")
    print(f"📈 Total in database: {total_count}")
    
    return total_count

def run_multiple_safe():
    """Run multiple safe collections to reach 100+ records"""
    target_records = 100
    current_count = get_total_records_count()
    
    print(f"🎯 Target: {target_records} records")
    print(f"📊 Current: {current_count} records")
    
    run_count = 0
    while current_count < target_records and run_count < 3:
        run_count += 1
        print(f"\n--- Run #{run_count} ---")
        safe_pipeline()
        current_count = get_total_records_count()
        
        if current_count < target_records:
            wait_time = random.uniform(60, 90)  # 1-1.5 minutes between runs
            print(f"⏳ Waiting {wait_time:.0f} seconds before next run...")
            time.sleep(wait_time)
    
    print(f"\n✅ Final count: {current_count} records")
    return current_count

if __name__ == "__main__":
    run_multiple_safe()
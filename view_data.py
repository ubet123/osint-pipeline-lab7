# view_data.py
import sqlite3
import pandas as pd

def view_all_data():
    conn = sqlite3.connect("data/osint.db")
    
    # Get all records
    df = pd.read_sql("SELECT * FROM osint_data", conn)
    conn.close()
    
    print(f"Total records: {len(df)}")
    print("\nAll records:")
    print(df.to_string())  # This shows ALL records without truncation
    
    # Statistics
    if 'sentiment' in df.columns:
        print(f"\n📊 Sentiment Statistics:")
        print(f"Average sentiment: {df['sentiment'].mean():.3f}")
        print(f"Positive records: {len(df[df['sentiment'] > 0])}")
        print(f"Negative records: {len(df[df['sentiment'] < 0])}")
        print(f"Neutral records: {len(df[df['sentiment'] == 0])}")
        print(f"Platform distribution:")
        print(df['platform'].value_counts())

if __name__ == "__main__":
    view_all_data()
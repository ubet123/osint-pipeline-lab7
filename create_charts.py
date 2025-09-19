# create_charts.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def create_sentiment_chart():
    conn = sqlite3.connect("data/osint.db")
    df = pd.read_sql("SELECT * FROM osint_data", conn)
    conn.close()
    
    # Sentiment distribution
    plt.figure(figsize=(10, 6))
    df['sentiment'].hist(bins=20)
    plt.title('Sentiment Distribution of OSINT Data')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Frequency')
    plt.savefig('screenshots/sentiment_distribution.png')
    
    # Platform distribution
    plt.figure(figsize=(10, 6))
    df['platform'].value_counts().plot(kind='bar')
    plt.title('Data Collection by Platform')
    plt.xlabel('Platform')
    plt.ylabel('Number of Records')
    plt.savefig('screenshots/platform_distribution.png')
    
    print("Charts saved to screenshots/ folder")

if __name__ == "__main__":
    create_sentiment_chart()
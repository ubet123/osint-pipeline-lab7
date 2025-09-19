import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

def plot_sentiment(db_path="data/osint.db"):
    # Connect to database and load table
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM osint_data", conn)
    conn.close()

    # Compute sentiment for each record
    df["sentiment"] = df["text"].apply(lambda x: TextBlob(x).sentiment.polarity)

    # Plot average sentiment by platform
    df.groupby("platform")["sentiment"].mean().plot(kind="bar")
    plt.title("Average Sentiment by Platform")
    plt.ylabel("Average Sentiment Polarity")
    plt.xlabel("Platform")
    plt.show()

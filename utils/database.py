# utils/database.py
import sqlite3
import os

def save_to_db(records, db_path="data/osint.db"):
    if not records:
        print("⚠️ No records to save")
        return
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # First, check if the table exists and has the right schema
    cur.execute("PRAGMA table_info(osint_data)")
    existing_columns = [col[1] for col in cur.fetchall()]
    
    # If table doesn't exist or has wrong schema, recreate it
    if not existing_columns or 'sentiment' not in existing_columns:
        print("🔄 Creating/updating database schema...")
        # Drop old table if exists
        cur.execute("DROP TABLE IF EXISTS osint_data")
        
        # Create new table with correct schema
        cur.execute("""
        CREATE TABLE osint_data (
            platform TEXT,
            user TEXT,
            timestamp TEXT,
            text TEXT,
            url TEXT,
            sentiment REAL
        )""")
    
    # Insert records
    success_count = 0
    for r in records:
        try:
            sentiment = r.get("sentiment", 0.0)
            cur.execute("INSERT INTO osint_data VALUES (?, ?, ?, ?, ?, ?)",
                       (r["platform"], r["user"], r["timestamp"], r["text"], 
                        r["url"], sentiment))
            success_count += 1
        except Exception as e:
            print(f"Database insert error: {e}")
    
    conn.commit()
    conn.close()
    print(f"💾 Saved {success_count}/{len(records)} records to database")


def get_total_records_count(db_path="data/osint.db"):
    """Helper function to count total records in database"""
    try:
        if not os.path.exists(db_path):
            return 0
            
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM osint_data")
        count = cur.fetchone()[0]
        conn.close()
        return count
    except:
        return 0
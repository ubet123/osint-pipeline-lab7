# fix_database.py
import sqlite3

def fix_database_schema():
    """Fix the database schema to include sentiment column"""
    conn = sqlite3.connect("data/osint.db")
    cur = conn.cursor()
    
    # Check if sentiment column exists
    cur.execute("PRAGMA table_info(osint_data)")
    columns = [col[1] for col in cur.fetchall()]
    
    if 'sentiment' not in columns:
        print("Adding sentiment column to database...")
        
        # Create temporary table with correct schema
        cur.execute("""
        CREATE TABLE IF NOT EXISTS osint_data_new (
            platform TEXT,
            user TEXT,
            timestamp TEXT,
            text TEXT,
            url TEXT,
            sentiment REAL
        )""")
        
        # Copy data from old table
        cur.execute("INSERT INTO osint_data_new SELECT *, 0.0 FROM osint_data")
        
        # Drop old table and rename new one
        cur.execute("DROP TABLE osint_data")
        cur.execute("ALTER TABLE osint_data_new RENAME TO osint_data")
        
        print("Database schema fixed successfully!")
    else:
        print("Database schema is already correct.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_database_schema()
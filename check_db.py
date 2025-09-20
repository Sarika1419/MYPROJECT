import sqlite3

def show_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    print(f"\n📂 Database: {db_name}")
    # Get tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()

    for table in tables:
        print(f"\n🟢 Table: {table[0]}")
        c.execute(f"SELECT * FROM {table[0]} LIMIT 5")
        rows = c.fetchall()
        for row in rows:
            print(row)

    conn.close()

# Show both DBs
show_db("users.db")
show_db("glowcare.db")

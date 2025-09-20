import sqlite3

def list_tables(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    conn.close()
    print(f"📂 Tables in {db_name}: {[t[0] for t in tables]}")

list_tables("users.db")
list_tables("glowcare.db")

import sqlite3

conn = sqlite3.connect("glowcare.db")
c = conn.cursor()

# Add username column if not exists
c.execute("ALTER TABLE new_user_responses ADD COLUMN username TEXT;")

conn.commit()
conn.close()

import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

# Remove duplicates (keep only the first entry for each username)
c.execute("""
    DELETE FROM users
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM users
        GROUP BY username
    )
""")

conn.commit()
conn.close()
print("✅ Duplicates removed from users table")

import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

# Remove duplicates keeping only first occurrence
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

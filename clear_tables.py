import sqlite3

def clear_table(db_name, table_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(f"DELETE FROM {table_name};")  # delete all rows
    conn.commit()
    conn.close()
    print(f"✅ Cleared data from {db_name}.{table_name}")

# Clear users table
clear_table("users.db", "users")

# Clear both questionnaire tables
clear_table("glowcare.db", "new_user_responses")
clear_table("glowcare.db", "returning_user_responses")

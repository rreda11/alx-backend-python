import sqlite3
import functools
from datetime import datetime  # ⬅️ Added for timing execution

# Decorator to log SQL queries and execution time
def log_queries():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else '')
            print(f"[LOG] Executing SQL Query: {query}")
            start_time = datetime.now()  # Start timer

            result = func(*args, **kwargs)

            end_time = datetime.now()  # End timer
            duration = (end_time - start_time).total_seconds()
            print(f"[LOG] Query executed in {duration:.4f} seconds")
            return result
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query and execution time
users = fetch_all_users(query="SELECT * FROM users")
print(users)

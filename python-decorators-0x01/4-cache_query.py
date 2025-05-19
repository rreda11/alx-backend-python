import time
import sqlite3 
import functools

# Reuse from previous tasks
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# New: Caching decorator
def cache_results(func):
    cache = {}  # Shared cache dictionary

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            print("[CACHE] Returning cached result.")
            return cache[key]
        print("[CACHE] No cache found. Executing query.")
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    return wrapper

@with_db_connection
@cache_results
def fetch_users_cached(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# First call (executes query)
users1 = fetch_users_cached()
print(users1)

# Second call (returns cached result)
users2 = fetch_users_cached()
print(users2)

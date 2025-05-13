import seed

def stream_users():
  db = seed.connect_db()
  seed.connect_to_prodev(db)
  seed.create_database(db)
  seed.create_table(db)
  seed.insert_data(db)

  cursor = db.cursor()
  yield from cursor.execute("SELECT * FROM user_data;")
    
  cursor.close()
  db.close()

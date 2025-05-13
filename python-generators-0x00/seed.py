from errno import errorcode
import mysql.connector
import uuid
import csv
import os



def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )



def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    print("Database 'ALX_prodev' is ready.")




def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )



def create_table(connection):
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS user_data (user_id CHAR(36) PRIMARY KEY,name VARCHAR(255) NOT NULL,email VARCHAR(255) NOT NULL,age DECIMAL(3,0) NOT NULL,UNIQUE(email))")
    print("Table 'user_data' is ready.")

    cursor.close()



def insert_data(connection, csv_file_path):
    """
    Reads data from a CSV file and inserts into user_data table.
    Generates a UUID for each record and avoids duplicates based on email.

    CSV file must have columns: name, email, age
    """
    cursor = connection.cursor()

    # Check if file exists
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file not found at {csv_file_path}")
        return

    # Track statistics
    rows_read = 0
    rows_inserted = 0
    rows_skipped = 0

    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)

            # Validate required columns
            required_columns = {'name', 'email', 'age'}
            if not required_columns.issubset(set(csv_reader.fieldnames)):
                missing = required_columns - set(csv_reader.fieldnames)
                print(f"Error: CSV file is missing required columns: {missing}")
                return

            # Process each row in the CSV
            for row in csv_reader:
                rows_read += 1

                # Extract and validate data
                name = row['name'].strip()
                email = row['email'].strip()

                # Make sure age is numeric
                try:
                    age = int(row['age'])
                except ValueError:
                    print(f"Skipping row with invalid age: {row['age']} for {email}")
                    rows_skipped += 1
                    continue

                # Generate a UUID for user_id
                user_id = str(uuid.uuid4())

                # Insert data
                try:
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))
                    rows_inserted += 1
                except IntegrityError as e:
                    if e.errno == errorcode.ER_DUP_ENTRY:
                        print(f"Skipping duplicate email: {email}")
                        rows_skipped += 1
                    else:
                        raise

                # Commit periodically (every 100 rows)
                if rows_inserted % 100 == 0:
                    connection.commit()
                    print(f"Processed {rows_inserted} rows so far...")

    except Exception as e:
        print(f"Error processing CSV file: {e}")
        # Roll back any pending changes
        connection.rollback()
    finally:
        # Final commit of any remaining changes
        connection.commit()
        cursor.close()

    # Print summary
    print(f"CSV import complete: {rows_read} rows read, {rows_inserted} inserted, {rows_skipped} skipped")

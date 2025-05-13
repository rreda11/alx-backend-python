import seed 

def stream_user_ages():
    db = seed.connect_to_prodev()
    cursor = db.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # 1st loop
        yield age

    cursor.close()
    db.close()


def calculate_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():  # 2nd loop
        total += age
        count += 1

    average = total / count if count else 0
    print(f"Average age of users: {average:.2f}")

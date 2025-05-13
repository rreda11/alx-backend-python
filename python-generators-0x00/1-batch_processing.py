
import seed 

def stream_users_in_batches(batch_size):
    db = seed.connect_to_prodev()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    db.close()


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):  # 1st loop
        for user in batch:  # 2nd loop
            if user[3] > 25:  # user[3] = age
                yield user  # yields one user at a time


for user in batch_processing(5):  # 3rd loop
        print(user)
return

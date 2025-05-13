import seed  

def paginate_users(page_size, offset):
    db = seed.connect_to_prodev()
    cursor = db.cursor()
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def lazy_paginate(page_size):
    while True:  
        page = paginate_users(page_size, offset)
        if not page:
            break
        for user in page:
            yield user
        offset += page_size

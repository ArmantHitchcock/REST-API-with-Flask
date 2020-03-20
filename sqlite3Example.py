import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)
create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)
"""
user = (1, 'jose', 'asdf')
users = [(2, 'wqwe', 'asdf'), (3, 'vghfgh', 'asdf'), (4, 'joshjke', 'asdf'), (5, 'cbcv', 'asdf'), (6, 'iolu', 'asdf')]
items = [('chair', 15.33), ('desk', 5.45), ('screen', 9.85), ('box', 0.60), ('mouse', 5.44), ('page', 1.00), ('cup', 2.10)]
insert_query = "INSERT INTO users VALUES (?,?,?)"
insert_query2 = "INSERT INTO items VALUES (Null, ?,?)"

cursor.execute(insert_query, user)
cursor.executemany(insert_query, users)
cursor.executemany(insert_query2, items)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

select_query2 = "SELECT * FROM items"
for row in cursor.execute(select_query2):
    print(row)
"""
connection.commit()
connection.close()

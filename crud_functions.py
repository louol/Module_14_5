import sqlite3

def initiate_db():
    connection = sqlite3.connect('not_telegram.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
            id INTEGER PRIMARY KEY, 
            title TEXT NOT NULL,
            description TEXT, 
            price INTEGER NOT NULL)''')
    cursor.execute('''
           CREATE TABLE IF NOT EXISTS Users(
           id INTEGER PRIMARY KEY,
           username TEXT NOT NULL,
           email TEXT NOT NULL,
           age INTEGER NOT NULL,
           balance INTEGER NOT NULL)''')
    #cursor.execute('DELETE FROM Users WHERE id >= 0') #Очистка таблицы Users
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('not_telegram.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    return cursor.fetchall()
    connection.close()

def add_user(username, email, age):
    connection = sqlite3.connect('not_telegram.db')
    cursor = connection.cursor()
    check_user = cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
    if check_user.fetchone() is None:
        cursor.execute(
            "INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",
            (username, email, age, 1000)
        )
    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('not_telegram.db')
    cursor = connection.cursor()
    check_user = cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
    if check_user.fetchone() is None:
        return True
    else:
        return False
    connection.commit()
    connection.close()


if __name__ == '__main__':
    initiate_db()






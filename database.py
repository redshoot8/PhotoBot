import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('data/database.db')
        self.cursor = self.connection.cursor()

    def users_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        locale TEXT NOT NULL
        )
        ''')
        self.connection.commit()

    def images_table(self):
        pass

    def add_user(self, user_id, user_locale):
        self.cursor.execute('INSERT INTO Users (id, locale) VALUES (?, ?)', (user_id, user_locale))
        self.connection.commit()

    def update_user(self, user_id, new_locale):
        self.cursor.execute('UPDATE Users SET locale = ? WHERE id = ?', (new_locale, user_id))
        self.connection.commit()

    def custom_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.fetchall()


if __name__ == '__main__':
    db = Database()
    db.users_table()
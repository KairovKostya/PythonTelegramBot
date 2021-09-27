import sqlite3


class SQL:
    """This class is just database"""
    database: str
    def __init__(self, data):
        database = data
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        self.cur.execute('''
                            CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            first_name VARCHAR(255),
                            last_name VARCHAR(255)
                                )''')
        self.conn.commit()

    def subscriber_exists(self, user_id):
        with self.conn:
            result = self.cur.execute('''
                SELECT * FROM users WHERE id = ?''', (user_id,)).fetchall()
            return bool(len(result))

    def add_users(self, usr):
        with self.conn:
            self.cur.execute("INSERT INTO 'users' ('id', 'first_name', 'last_name') VALUES(?,?,?)",
                        (usr.id, usr.first_name, usr.last_name))
            self.conn.commit()

    def get_subscriptions(self):
        with self.conn:
            return self.cur.execute("SELECT * FROM 'users' ")

    def remove_subscription(self, user_id):
        with self.conn:
            self.cur.execute("DELETE FROM users WHERE id = ?", (user_id,)).fetchall()
            self.conn.commit()

    def get_len(self):
        with self.conn:
            self.cur.execute("SELECT COUNT(*) FROM users")
            count = self.cur.fetchone()[0]
            return count




import hashlib
import sqlite3
from tov import Tovar
class Database:
    
    def __init__(self):
        self.conn = sqlite3.connect('phone_store_db.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT,
                full_name TEXT
            )
        ''')     
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                full_name TEXT
            )           
        '''  )
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tovars (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                price INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                tovar_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (tovar_id) REFERENCES tovars (id)
            )
        ''')
        self.conn.commit()
    
    def add_user(self, username, password, role, full_name):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute('''
            INSERT INTO users (username, password, role, full_name)
            VALUES (?, ?, ?, ?)
        ''', (username, hashed_password, role, full_name))
        self.conn.commit()

    def get_user_by_username(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()

    def add_employee(self, username, password, full_name):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute('''
            INSERT INTO employees (username, password, full_name)
            VALUES (?, ?, ?)
        ''', (username, hashed_password, full_name))
        self.conn.commit()

    def add_tovar(self, name, price):
        if not isinstance(price, (int, float)) or price < 2000:
            print("Ошибка: Цена должна быть быть больше.")
            return

        self.cursor.execute('''
            INSERT INTO tovars (name, price)
            VALUES (?, ?)
        ''', (name, price)) 
        self.conn.commit()

    def drop_tovars_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS tovars')
        self.conn.commit()

    def get_all_tovars(self):
        self.cursor.execute('SELECT * FROM tovars')
        rows = self.cursor.fetchall()
        tovars = []
        for row in rows:
            tovar = Tovar(row[1], row[2])
            tovars.append(tovar)
        return tovars

    def add_order(self, user_id, tovar_id):
        self.cursor.execute('''
            INSERT INTO orders (user_id, tovar_id)
            VALUES (?, ?)
        ''', (user_id, tovar_id))
        self.conn.commit()
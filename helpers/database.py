import sqlite3
from config.db_config import Config

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE
                             TABLE IF NOT EXISTS
                             products (
                             product_title TEXT,
                             product_price REAL,
                             path_to_image TEXT
                             )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS cache (
                             product_title TEXT,
                             product_price REAL
                             )''')
        self.conn.commit()

    def get_cached_price(self, title):
        self.cursor.execute("SELECT product_price FROM cache WHERE product_title = ?", (title,))
        cached_price = self.cursor.fetchone()
        return cached_price[0] if cached_price else None

    def store_cache_price(self, title, price):
        self.cursor.execute("INSERT INTO cache VALUES (?, ?)", (title, price))
        self.conn.commit()

    def insert_product(self, product):
        self.cursor.execute("INSERT INTO products VALUES (?, ?, ?)", (product.product_title, product.product_price, product.path_to_image))
        self.conn.commit()

    def close(self):
        self.conn.close()
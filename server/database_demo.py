import sqlite3

class Database():
    def __init__(self):
        # Connect to the SQLite database
        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()
        self.user = None

        # Create the Users table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        # Create the Books table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                published_year INTEGER
            )
        """)

        # Add an admin user
        self.cursor.execute("""
            INSERT INTO Users (username, password, role)
            VALUES (?, ?, ?)
        """, ("admin", "admin_password", "admin"))

        # Add a regular user
        self.cursor.execute("""
            INSERT INTO Users (username, password, role)
            VALUES (?, ?, ?)
        """, ("user", "user_password", "user"))

        # Add some books
        self.cursor.execute("""
            INSERT INTO Books (title, author, published_year)
            VALUES (?, ?, ?)
        """, ("Book 1", "Author 1", 2020))

        self.cursor.execute("""
            INSERT INTO Books (title, author, published_year)
            VALUES (?, ?, ?)
        """, ("Book 2", "Author 2", 2019))

        self.conn.commit()

    def add_user(self, username, password, role):
        self.cursor.execute("""
            INSERT INTO Users (username, password, role)
            VALUES (?, ?, ?)
        """, (username, password, role))
        self.conn.commit()
    
    def login(self, username, password):
        self.cursor.execute("SELECT username, password, role, id FROM Users WHERE username=?", (username,))
        user = self.cursor.fetchone()
        if (user and user[1] == password):
            self.user = user
            return user
        return None
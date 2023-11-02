import sqlite3

class Database():
    def __init__(self):
        # Connect to the SQLite database
        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()

        # Create the Users table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        # Create the Catalog table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Catalog (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                published_year INTEGER
            )
        """)
        try:
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
            
            
        except:
            pass

        self.conn.commit()

    def add_user(self, username, password, role):
        try:
            self.cursor.execute("""
                INSERT INTO Users (username, password, role)
                VALUES (?, ?, ?)
            """, (username, password, role))
            self.conn.commit()

            self.cursor.execute("SELECT username, password, role, id FROM Users WHERE username=?", (username,))
            return self.cursor.fetchone()
        except:
            return None
    
    def login(self, username, password):
        self.cursor.execute("SELECT username, password, role, id FROM Users WHERE username=?", (username,))
        user = self.cursor.fetchone()
        if (user and user[1] == password):
            return user
        return None
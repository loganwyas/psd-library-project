import sqlite3
import json

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
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                release INTEGER
            )
        """)
        
        # Create the Libraries table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Libraries (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                latitude REAL,
                longitude REAL
            )
        """)
        
        # Create the ItemCounts table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ItemCounts (
                library_id INTEGER,
                item_id INTEGER,
                count INTEGER,
                PRIMARY KEY(library_id, item_id),
                FOREIGN KEY(library_id) REFERENCES Libraries(id),
                FOREIGN KEY(item_id) REFERENCES Catalog(id)
            )
        """)
        
        # Create the UserItemStatus table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserItemStatus (
                user_id INTEGER,
                library_id INTEGER,
                item_id INTEGER,
                status TEXT NOT NULL,
                date INTEGER,
                PRIMARY KEY(user_id, library_id, item_id),
                FOREIGN KEY(user_id) REFERENCES Users(id),
                FOREIGN KEY(library_id) REFERENCES Libraries(id),
                FOREIGN KEY(item_id) REFERENCES Catalog(id)
            )
        """)
        
        try:           
            # Add initial data to the database
            with open("initial_data.json", "r") as file:
                data = json.load(file)
                
                for user in data["users"]:
                    self.cursor.execute("""
                        INSERT INTO Users (username, password, role)
                        VALUES (?, ?, ?)
                    """, (user["username"], user["password"], user["role"]))
                    
                catalog = data["catalog"]
                for itemType in ["book", "videoGame", "movie"]:
                    items = catalog[itemType]
                    for item in items:
                        self.cursor.execute("""
                            INSERT INTO Catalog (type, title, author, release)
                            VALUES (?, ?, ?, ?)
                        """, (itemType, item["title"], item["author"], item["release"]))
                        
                for library in data["libraries"]:
                    self.cursor.execute("""
                        INSERT INTO Libraries (name, latitude, longitude)
                        VALUES (?, ?, ?)
                    """, (library["name"], library["latitude"], library["longitude"]))
                    
                for count in data["counts"]:
                    self.cursor.execute("""
                        INSERT INTO ItemCounts (library_id, item_id, count)
                        VALUES (?, ?, ?)
                    """, (count["library"], count["item"], count["count"]))
                        
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
    
    def get_catalog(self, search):
        param = "%" + search + "%"
        self.cursor.execute("SELECT * FROM Catalog WHERE UPPER(title) LIKE UPPER(?) OR UPPER(author) LIKE UPPER(?)", (param,param))
        items = self.cursor.fetchall()
        return items
import sqlite3
import json
import time

def get_time():
    return round(time.time() * 1000)

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
                role TEXT NOT NULL,
                name TEXT,
                profilePic TEXT
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
        
        # Create the Librarians table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Librarians (
                user_id INTEGER,
                library_id INTEGER,
                PRIMARY KEY(user_id, library_id),
                FOREIGN KEY(user_id) REFERENCES Users(id),
                FOREIGN KEY(library_id) REFERENCES Libraries(id)
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
                    
                for librarian in data["librarians"]:
                    self.cursor.execute("""
                        INSERT INTO Librarians (user_id, library_id)
                        VALUES (?, ?)
                    """, (librarian["user"], librarian["library"]))
                    
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

            self.cursor.execute("SELECT username, password, role, id, name, profilePic FROM Users WHERE username=?", (username,))
            return self.cursor.fetchone()
        except:
            return None
    
    def login(self, username, password):
        self.cursor.execute("SELECT username, password, role, id, name, profilePic FROM Users WHERE username=?", (username,))
        user = self.cursor.fetchone()
        if (user and user[1] == password):
            return user
        return None
    
    def change_user_info(self, username, password, name, profilePic):
        try:
            self.cursor.execute("UPDATE Users SET password=?, name=?, profilePic=? WHERE username=?", (password, name, profilePic, username))
            self.conn.commit()
            return {"username": username}
        except:
            return
        
    
    def get_catalog(self, search):
        param = "%" + search + "%"
        self.cursor.execute("SELECT * FROM Catalog WHERE UPPER(title) LIKE UPPER(?) OR UPPER(author) LIKE UPPER(?)", (param,param))
        results = self.cursor.fetchall()
        items = []
        for result in results:
            item = self.get_item_from_id(result[0])
            items.append(item)
        return items
    
    def get_item_from_id(self, item_id):
        self.cursor.execute("SELECT * FROM Catalog WHERE id=?", (item_id,))
        item = self.cursor.fetchone()
        if item:
            val = {
                "id": item[0],
                "type": item[1],
                "title": item[2],
                "author": item[3],
                "release": item[4],
            }
            return val
    
    def get_items_from_library(self, library_id):
        self.cursor.execute("SELECT * FROM ItemCounts WHERE library_id=?", (library_id,))
        items = self.cursor.fetchall()
        if items:
            formattedItems = []
            for val in items:
                catalogItem = self.get_item_from_id(val[1])
                if catalogItem:
                    catalogItem["count"] = val[2]
                    formattedItems.append(catalogItem)
            return formattedItems
        
    def get_unadded_library_items(self, library_id):
        self.cursor.execute("SELECT * FROM Catalog WHERE NOT EXISTS (SELECT * FROM ItemCounts WHERE ItemCounts.library_id=? AND ItemCounts.item_id=Catalog.id)", (library_id,))
        items = self.cursor.fetchall()
        if items:
            formattedItems = []
            for val in items:
                catalogItem = self.get_item_from_id(val[0])
                if catalogItem:
                    formattedItems.append(catalogItem)
            return formattedItems
    
    def get_library_from_id(self, library_id):
        self.cursor.execute("SELECT * FROM Libraries WHERE id=?", (library_id,))
        val = self.cursor.fetchone()
        if val:
            catalog = self.get_items_from_library(val[0])
            library = {
                "id": val[0],
                "name": val[1],
                "latitude": val[2],
                "longitude": val[3],
                "catalog": catalog
            }
            return library
    
    def get_library_from_user(self, user_id):
        self.cursor.execute("SELECT * FROM Librarians WHERE user_id=?", (user_id,))
        librarian = self.cursor.fetchone()
        if librarian:
            library = self.get_library_from_id(librarian[1])
            return library
        
    def add_library_item_count(self, library, item, count):
        self.cursor.execute("""
            INSERT INTO ItemCounts (library_id, item_id, count)
            VALUES (?, ?, ?)
        """, (library, item, count))
        self.conn.commit()
        
        self.cursor.execute("SELECT * FROM ItemCounts WHERE library_id=? AND item_id=?", (library, item))
        item = self.cursor.fetchone()
        if item:
            return item
        
    def set_library_item_count(self, library, item, count):
        self.cursor.execute("UPDATE ItemCounts SET count=? WHERE library_id=? AND item_id=?", (count, library, item))
        self.conn.commit()
        
        self.cursor.execute("SELECT * FROM ItemCounts WHERE library_id=? AND item_id=?", (library, item))
        item = self.cursor.fetchone()
        if item:
            return item
        
    def remove_library_item(self, library, item):
        self.cursor.execute("DELETE FROM ItemCounts WHERE library_id=? AND item_id=?", (library, item))
        self.conn.commit()
        
        self.cursor.execute("SELECT * FROM ItemCounts WHERE library_id=? AND item_id=?", (library, item))
        item = self.cursor.fetchone()
        return not item

    def put_item_hold(self, user_id, library_id, item_id, status, date):
        try:
            # Check if the user is a librarian for the specified library
            self.cursor.execute("SELECT * FROM Librarians WHERE user_id=? AND library_id=?", (user_id, library_id))
            librarian = self.cursor.fetchone()
            if librarian:
                # Check if the item exists in the library
                self.cursor.execute("SELECT * FROM ItemCounts WHERE library_id=? AND item_id=?", (library_id, item_id))
                item_count = self.cursor.fetchone()
                if item_count:
                    # Insert or update the hold status in UserItemStatus table
                    self.cursor.execute("""
                        INSERT OR REPLACE INTO UserItemStatus (user_id, library_id, item_id, status, date)
                        VALUES (?, ?, ?, ?, ?)
                    """, (user_id, library_id, item_id, status, date))
                    self.conn.commit()

                    return True  # Successfully put the item on hold
        except sqlite3.Error as e:
            print("SQLite error:", e)

        return False  # Failed to put the item on hold

    def checkout_item(self, user_id, library_id, item_id):
        self.cursor.execute("""
            INSERT OR REPLACE INTO UserItemStatus (user_id, library_id, item_id, status, date)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, library_id, item_id, "checked_out", get_time()))
        self.conn.commit()
        
    def get_user_items(self, user_id):
        self.cursor.execute("SELECT * FROM UserItemStatus WHERE user_id=?", (user_id,))
        raw_items = self.cursor.fetchall()
        items = []
        for raw_item in raw_items:
            item = {
                "user_id": raw_item[0],
                "library_id": raw_item[1],
                "item_id": raw_item[2],
                "status": raw_item[3],
                "date": raw_item[4]
            }
            items.append(item)
        return items
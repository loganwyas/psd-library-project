import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create the Users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
""")

# Create the Books table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        published_year INTEGER
    )
""")

# Add an admin user
cursor.execute("""
    INSERT INTO Users (username, password, role)
    VALUES (?, ?, ?)
""", ("admin", "admin_password", "admin"))

# Add a regular user
cursor.execute("""
    INSERT INTO Users (username, password, role)
    VALUES (?, ?, ?)
""", ("user", "user_password", "user"))

# Add some books
cursor.execute("""
    INSERT INTO Books (title, author, published_year)
    VALUES (?, ?, ?)
""", ("Book 1", "Author 1", 2020))

cursor.execute("""
    INSERT INTO Books (title, author, published_year)
    VALUES (?, ?, ?)
""", ("Book 2", "Author 2", 2019))

# Commit the changes and close the database connection
conn.commit()
conn.close()

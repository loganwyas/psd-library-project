from database import Database
import string
import random
import time

def getRandomString():
    return ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=10))

def test_login():
    db = Database()
    user = db.login("admin", "password")
    assert (user and user[2] == "admin")
        
def test_failed_login():
    db = Database()
    user = db.login("user", "not_the_password")
    assert not user
    
def test_add_user():
    db = Database()
    username = getRandomString()
    user = db.add_user(username, "secure_password", "user")
    assert (user and user[2] == "user" and user[0] == username)
        
def test_failed_add_user():
    db = Database()
    user = db.add_user("user", "different_password", "user")
    assert not user
    
def test_get_catalog_empty():
    db = Database()
    catalog = db.get_catalog("This is not a book that has ever existed")
    assert len(catalog) == 0
    
def test_get_catalog_one_item():
    db = Database()
    catalog = db.get_catalog("mine")
    assert len(catalog) == 1
    
def test_get_item_from_id():
    db = Database()
    item = db.get_item_from_id(1)
    assert (item and item["author"] == "J.K. Rowling" and item["release"] == 1997)
        
def test_failed_get_item_from_id():
    db = Database()
    item = db.get_item_from_id(174391838941)
    assert not item
    
def test_get_library_from_id():
    db = Database()
    library = db.get_library_from_id(10)
    assert (library and library["name"] == "Sunnydale Library" and len(library["catalog"]) == 15)
        
def test_failed_get_library_from_id():
    db = Database()
    library = db.get_library_from_id(58390143415890)
    assert not library
    
def test_get_library_from_user():
    db = Database()
    library = db.get_library_from_user(3)
    assert (library and library["id"] == 3)
    
def test_failed_get_library_from_user():
    db = Database()
    library = db.get_library_from_user(7838941)
    assert not library

def test_get_item_from_id():
    db = Database()
    item_id = 1  # Replace with the actual item ID in your database
    expected_author = "J.K. Rowling"  # Replace with the actual expected author value
    expected_release = 1997  # Replace with the actual expected release year

    item = db.get_item_from_id(item_id)
    assert (item and item["author"] == expected_author and item["release"] == expected_release)

def test_put_item_hold_by_librarian():
    db = Database()
    
    # Assuming you have a librarian user and a library in your database
    librarian_user_id = 1  # Replace with the actual librarian user ID
    library_id = 1  # Replace with the actual library ID
    item_id = 1  # Replace with the actual item ID
    
    # Use a unique status and date for each test to avoid conflicts
    status = getRandomString()
    date = int(time.time())  # Current timestamp
    
    success = db.put_item_hold(librarian_user_id, library_id, item_id, status, date)
    assert success

def test_put_item_hold_without_librarian_privileges():
    db = Database()
    
    # Assuming you have a regular user and a library in your database
    user_id = 2  # Replace with the actual regular user ID
    library_id = 1  # Replace with the actual library ID
    item_id = 1  # Replace with the actual item ID
    
    # Use a unique status and date for each test to avoid conflicts
    status = getRandomString()
    date = int(time.time())  # Current timestamp
    
    success = db.put_item_hold(regular_user_id, library_id, item_id, status, date)
    assert not success

def test_put_item_hold_in_nonexistent_library():
    db = Database()
    
    # Assuming you have a user and a non-existent library ID
    user_id = 3  # Replace with the actual user ID
    nonexistent_library_id = 9999  # Replace with a non-existent library ID
    item_id = 1  # Replace with the actual item ID
    
    # Use a unique status and date for each test to avoid conflicts
    status = getRandomString()
    date = int(time.time())  # Current timestamp
    
    success = db.put_item_hold(user_id, nonexistent_library_id, item_id, status, date)
    assert not success

        
if __name__ == '__main__':
    db = Database()
    print(db.get_catalog(""))

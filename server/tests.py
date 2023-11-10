from database import Database
import string
import random

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
        
if __name__ == '__main__':
    db = Database()
    print(db.get_catalog(""))
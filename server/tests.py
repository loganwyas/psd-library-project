from database import Database
import string
import random

def getRandomString():
    return ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=10))

def test_login():
    db = Database()
    user = db.login("admin", "password")
    if user:
        assert user[2] == "admin"
    else:
        assert False
        
def test_failed_login():
    db = Database()
    user = db.login("user", "not_the_password")
    assert not user
    
def test_add_user():
    db = Database()
    username = getRandomString()
    user = db.add_user(username, "secure_password", "user")
    if user:
        assert user[2] == "user" and user[0] == username
    else:
        assert False
        
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
    if item:
        assert item["author"] == "J.K. Rowling" and item["release"] == 1997
    else:
        assert False
        
def test_failed_get_item_from_id():
    db = Database()
    item = db.get_item_from_id(174391838941)
    assert not item
        
if __name__ == '__main__':
    db = Database()
    print(db.get_catalog(""))
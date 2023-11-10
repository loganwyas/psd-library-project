from database import Database

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
    user = db.add_user("person", "secure_password", "user")
    if user:
        assert user[2] == "user" and user[0] == "person"
    else:
        assert False
        
def test_failed_add_user():
    db = Database()
    user = db.add_user("user", "different_password", "user")
    assert not user
        
if __name__ == '__main__':
    db = Database()
    print(db.get_catalog(""))
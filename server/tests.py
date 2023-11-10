from database import Database

def test_login():
    db = Database()
    user = db.login("user", "password")
    print(db.get_catalog(""))
    if user:
        assert user[2] == "user"
    else:
        assert False
        
if __name__ == '__main__':
    db = Database()
    print(db.get_catalog(""))
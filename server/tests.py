from database import Database

def test_login():
    db = Database()
    user = db.login("user", "password")
    assert (user and user[2] == "user")
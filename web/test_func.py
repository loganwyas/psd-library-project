import pytest
from add_readerandbook import app, db, Book, User


@pytest.fixture
def client():
    app.config.from_object('config.TestConfig')
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()


def test_index(client):
    response = client.get('/')
    #assert response.status_code == 200
    assert b"index.html" in response.data


def test_add_book(client):
    response = client.post('/add_book', data={
        'title': 'Test Book',
        'author': 'Test Author',
        'book code': '026'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"New book added!" in response.data




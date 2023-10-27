#from configure import Config
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.secret_key = 'some_secret_key'

db = SQLAlchemy(app)
#app.config.from_object(Config)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)  # unique code
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    checked_out_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


@app.route('/')
def index():
    books = Book.query.all()
    users = User.query.all()
    return render_template('index.html', books=books, users=users)


@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    code = request.form.get('book code')
    if title and author and code:
        new_book = Book(title=title, author=author, code=code)
        db.session.add(new_book)
        db.session.commit()
        flash("New book added!")
    return redirect(url_for('index'))


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    code = request.form.get('reader ID')
    if name:
        new_user = User(name=name,code=code)
        db.session.add(new_user)
        db.session.commit()
        flash("New reader added!")
    return redirect(url_for('index'))


@app.route('/checkout/<int:book_id>')
def checkout(book_id):
    user_id = request.args.get('user_id', type=int)
    book = Book.query.get(book_id)
    if book:
        if book.checked_out_by is None:
            book.checked_out_by = user_id
            db.session.commit()
            flash(f"{book.title} has been borrowed!")
        else:
            flash(f"{book.title} has been borrowed by others!")
    return redirect(url_for('index'))


@app.route('/checkin/<int:book_id>')
def checkin(book_id):
    book = Book.query.get(book_id)
    if book and book.checked_out_by:
        book.checked_out_by = None
        db.session.commit()
        flash(f"{book.title} has been returned")
    return redirect(url_for('index'))


def init_db():
    with app.app_context():
        db.create_all()
        #clear_books()

        books_data = [
    {"code": "001", "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"code": "002", "title": "1984", "author": "George Orwell"},
    {"code": "003", "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"code": "004", "title": "Pride and Prejudice", "author": "Jane Austen"},
    {"code": "005", "title": "Moby Dick", "author": "Herman Melville"},
    {"code": "006", "title": "War and Peace", "author": "Leo Tolstoy"},
    {"code": "007", "title": "The Catcher in the Rye", "author": "J.D. Salinger"},
    {"code": "008", "title": "Brave New World", "author": "Aldous Huxley"},
    {"code": "009", "title": "Jane Eyre", "author": "Charlotte Brontë"},
    {"code": "010", "title": "The Odyssey", "author": "Homer"},
    {"code": "011", "title": "Crime and Punishment", "author": "Fyodor Dostoyevsky"},
    {"code": "012", "title": "The Brothers Karamazov", "author": "Fyodor Dostoyevsky"},
    {"code": "013", "title": "The Lord of the Rings", "author": "J.R.R. Tolkien"},
    {"code": "014", "title": "One Hundred Years of Solitude", "author": "Gabriel García Márquez"},
    {"code": "015", "title": "The Picture of Dorian Gray", "author": "Oscar Wilde"},
    {"code": "016", "title": "Anna Karenina", "author": "Leo Tolstoy"},
    {"code": "017", "title": "Wuthering Heights", "author": "Emily Brontë"},
    {"code": "018", "title": "Don Quixote", "author": "Miguel de Cervantes"},
    {"code": "019", "title": "The Count of Monte Cristo", "author": "Alexandre Dumas"},
    {"code": "020", "title": "A Tale of Two Cities", "author": "Charles Dickens"},
    {"code": "021", "title": "The Grapes of Wrath", "author": "John Steinbeck"},
    {"code": "022", "title": "Ulysses", "author": "James Joyce"},
    {"code": "023", "title": "The Divine Comedy", "author": "Dante Alighieri"},
    {"code": "024", "title": "Les Misérables", "author": "Victor Hugo"},
    {"code": "025", "title": "Great Expectations", "author": "Charles Dickens"}
]

        for book_data in books_data:
            if not Book.query.filter_by(code=book_data["code"]).first():
                book = Book(code=book_data["code"], title=book_data["title"], author=book_data["author"])
                db.session.add(book)

        db.session.commit()
        print("Database initialized!")


def clear_books():
    Book.query.delete()
    db.session.commit()
    print("All books cleared!")



if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)

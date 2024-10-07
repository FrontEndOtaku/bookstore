from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True)
    author = db.Column(db.String(100), index=True)
    category = db.Column(db.String(50), index=True)
    year = db.Column(db.Integer)
    price = db.Column(db.Float)
    rental_price = db.Column(db.Float)
    availability = db.Column(db.Boolean, default=True)
    rentals = db.relationship('Rental', backref='book', lazy='dynamic')

    def __repr__(self):
        return '<Book {}>'.format(self.title)

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default="active")  # active, expired, returned

    def __repr__(self):
        return '<Rental {}>'.format(self.book_id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

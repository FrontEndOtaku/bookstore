from flask import render_template, redirect, flash, url_for, request
from app import app, db
from app.models import User, Book, Rental
from app.forms import RegistrationForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
@app.route('/index')
def index():
    books = Book.query.all()
    return render_template('index.html', title='Главная', books=books)

@app.route('/book/<int:id>')
def book(id):
    book = Book.query.get_or_404(id)
    return render_template('book.html', title=book.title, book=book)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    books = Book.query.all()
    return render_template('admin.html', title='Админ-панель', books=books)

@app.route('/rent/<int:book_id>')
@login_required
def rent_book(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.availability:
        flash('Книга недоступна для аренды.')
        return redirect(url_for('index'))

    # Создаем аренду на 2 недели (пример)
    rental = Rental(book_id=book.id, user_id=current_user.id, end_date=datetime.utcnow() + timedelta(weeks=2))
    db.session.add(rental)
    db.session.commit()
    flash('Книга успешно арендована!')
    return redirect(url_for('index'))

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    form = AddBookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, 
                    category=form.category.data, year=form.year.data,
                    price=form.price.data, rental_price=form.rental_price.data)
        db.session.add(book)
        db.session.commit()
        flash('Книга успешно добавлена!')
        return redirect(url_for('admin'))
    return render_template('add_book.html', title='Добавить книгу', form=form)


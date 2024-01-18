# routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
import secrets
from sqlalchemy import text

# Create a Blueprint for the routes
bp = Blueprint('routes', __name__)


# Define the get_user_name function
def get_user_name(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return f"{user.first_name} {user.last_name}"
    return None


@bp.route('/logout')
def logout():
    # Clear the 'user_id' from the session to indicate the user is logged out
    session.pop('user_id', None)
    
    return redirect(url_for('routes.home'))

@bp.route('/')
@bp.route('/home', methods=['GET', 'POST'])
def home():
    # Check if the user is logged in (you should have a proper login mechanism)
    logged_in = 'user_id' in session  # Assuming you store user_id in the session when the user logs in

    # If the user is logged in, you can retrieve the user's name from the database or session
    user_name = get_user_name(session.get('user_id'))  # Replace this with the appropriate function to get the user's name

    return render_template('home.html', logged_in=logged_in, user_name=user_name)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            return "Passwords do not match."

        # Check if the email has already been used
        if User.query.filter_by(email=email).first():
            return "Email address already in use."

        # Password validation (you can implement your criteria from lab7 here)

        # Create a new user and add to the database
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('routes.thankyou'))

    return render_template('signup.html')

@bp.route('/shop', methods=['GET','POST'])
def shop():
    return render_template('shop.html')

@bp.route('/about', methods=['GET','POST'])
def about():
    return render_template('about.html')


@bp.route('/contact', methods=['GET','POST'])
def contact():
    return render_template('contact.html')


# Assuming you have a "failed_login_attempts" and "is_locked" field in the User model
# Assuming you have a "failed_login_attempts" field in the User model

from datetime import datetime, timedelta

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the email exists in the database
        user = User.query.filter_by(email=email).first()
        if not user:
            return "User not found. Please sign up."

        # Check if the account is locked due to multiple failed login attempts
        if user.failed_login_attempts >= 5 and user.locked_until and user.locked_until > datetime.utcnow():
            return "Your account is locked due to multiple failed login attempts. Please try again later."

        # Check if the password matches
        if not check_password_hash(user.password, password):
            # Increment the failed login attempts
            user.failed_login_attempts += 1

            # Check if the threshold is exceeded
            if user.failed_login_attempts >= 5:
                # Lock the account for 30 minutes
                user.locked_until = datetime.utcnow() + timedelta(minutes=30)

            db.session.commit()
            return "Invalid password. Please try again."

        # Reset failed login attempts on successful login
        user.failed_login_attempts = 0
        user.locked_until = None
        db.session.commit()


        # Redirect to a secret page (you can implement this logic)
        return redirect(url_for('routes.secret_page'))

    return render_template('login.html')

@bp.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@bp.route('/secretpage')
def secret_page():
    return render_template('secretpage.html')
    
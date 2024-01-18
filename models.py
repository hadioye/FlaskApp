from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    failed_login_attempts = db.Column(db.Integer, default=0)
    username = db.Column(db.String(50), nullable=False, default="")  # Provide a default value
    locked_until = db.Column(db.DateTime, nullable=True)

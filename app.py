from flask import Flask, render_template, request, redirect, url_for
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from routes import bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

# Register the Blueprint
app.register_blueprint(bp)

def index():
    # Render the home.html template for the root URL
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():   #Run these two lines 
       db.drop_all()          #To clear database
    with app.app_context():
        db.create_all()
    app.run(debug=True)
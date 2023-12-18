from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secret key
app.config['SECRET_KEY'] = '0987654321'

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)

# Define the User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Set up the user loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create the tables within the application context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# User login page
@app.route('/user/user_login_page')
def user_login_page():
    return render_template('user/login.html')

# Admin login page
@app.route('/admin/admin_login_page')
def admin_login_page():
    return render_template('admin/login.html')

# User home page
@app.route('/user/templates/home_page')
@login_required  # This ensures that only logged-in users can access this page
def home_page():
    return render_template('user/templates/home.html')

# Admin home page
@app.route('/admin/templates/admin_page')
def admin_page():
    return render_template('admin/templates/admin.html')

# Login route and validation
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'].strip()
    password = request.form['password'].strip()

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        # Login the user
        login_user(user)
        # Redirect to the main page after successful login
        return redirect(url_for('home_page'))

    return render_template('user/templates/login_alert.html')

# Add a new user in login
@app.route('/add_user', methods=['POST'])
def add_user():
    new_username = request.form['new_username']
    new_password = request.form['new_password']

    if not new_username or not new_password:
        return 'Username and password are required.'

    hashed_password = generate_password_hash(new_password)

    new_user = User(username=new_username, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"status": "success", "message": f'User {new_username} added successfully! \n you may now Login'})
    except:
        db.session.rollback()
        return jsonify({"status": "error", "message": f'Username {new_username} already exists. Please choose a different username.'})

if __name__ == '__main__':
    app.run(debug=True)

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
    is_admin = db.Column(db.Boolean, default=False)

# Set up the user loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

# User login page
@app.route('/user/user_login_page')
def user_login_page():
    return render_template('index.html')

# Add a route for serving other static files (images, etc.)
@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

# about
@app.route('/about')
def about_page():
    return render_template('about.html')

# home page/index page
@app.route('/index_home')
def index_home ():
    return render_template('templates/index.html')

# Route for the login page
@app.route('/login')
def login():
    return render_template('index.html')

# Route for the sign-up page
@app.route('/signup')
def signup():
    return render_template('sign_up.html')

# products
@app.route('/product')
def product():
    return render_template('product.html')

# contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

# blog
@app.route('/blog')
def blog():
    return render_template('blog.html')

# feature
@app.route('/feature')
def feature():
    return render_template('feature.html')

# testimonial
@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')


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
        return redirect(url_for('index_home'))

    return render_template('templates/login_alert.html')

# Add a new user in login
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        is_admin = 'admin' in request.form

        if not new_username or not new_password:
            flash('Username and password are required.', 'danger')
        else:
            hashed_password = new_password  # You should hash the password in a real-world application
            new_user = User(username=new_username, password=hashed_password, is_admin=is_admin)

            db.session.add(new_user)
            db.session.commit()
            flash(f'User {new_username} added successfully!', 'success')
            return redirect(url_for('login'))

    return render_template('sign_up.html')

# subscriptional message
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')

    if not email or email in subscriptions:
        return jsonify({'status': 'error', 'message': 'Invalid or duplicate email'})

    subscriptions.add(email)
    return jsonify({'status': 'success', 'message': 'Subscription successful'})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

# Define a blueprint for routing
main = Blueprint('main', __name__)

@main.route('/')
def home():

    # `current_user` is always available, even for visitors
    if current_user.is_authenticated:
        message = f"Welcome back, {current_user.username}!"
    else:
        message = "Welcome to Plant-Swap!"

    return render_template('index.html', message=message)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Add authentication logic here
        # Example: Authenticate user and log them in
        # username = request.form['username']
        # password = request.form['password']
        # Authenticate user and call login_user(user) on success
        return redirect(url_for('main.home'))
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Add registration logic here
        # Example: Create a new user in the database
        # username = request.form['username']
        # email = request.form['email']
        # password = request.form['password']
        # Hash password and save user
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/user', methods=['GET', 'POST'])
@login_required
def user_domain():
    if request.method == 'POST':
        # Add logic to handle post creation
        # Example: Save the post data to the database
        # plant_type = request.form['plantType']
        # description = request.form['description']
        # photo = request.files['photo']
        # contact = request.form['contact']
        # Save the post
        return redirect(url_for('main.home'))
    return render_template('user_domain.html')


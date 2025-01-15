from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from geopy.geocoders import Nominatim
from .models import Post, SessionLocal

# Define a blueprint for routing
main = Blueprint('main', __name__)

@main.route('/', methods =['GET'])
def home():
    session = SessionLocal()
    location_filter = request.args.get('location')
    if location_filter:
        posts = session.query(Post).filter(Post.location_name.ilike(f"%{location_filter}%")).all()
    else:
        posts = session.query(Post).all()
    session.close()

    # Prepare data for the map
    map_data = [
        {
            "plant_type": post.plant_type,
            "description": post.description,
            "contact_info": post.contact_info,
            "latitude": post.latitude,
            "longitude": post.longitude,
            "location_name": post.location_name
        }
        for post in posts
    ]

    # `current_user` is always available, even for visitors
    if current_user.is_authenticated:
        message = f"Welcome back, {current_user.username}!"
    else:
        message = "Welcome to Plant-Swap!"

    return render_template('index.html', message=message, posts=posts, map_data=map_data)

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
    
@main.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        plant_type = request.form['plantType']
        description = request.form['description']
        contact_info = request.form['contact']
        location_name = request.form['location']
        photo = request.files['photo']  # Handle file uploads if applicable

        # Use geopy to get latitude and longitude
        geolocator = Nominatim(user_agent="plantswap")
        location = geolocator.geocode(location_name)
        if location is None:
            return "Invalid location", 400  # Handle invalid location gracefully

        # Save post to the database
        session = SessionLocal()
        post = Post(
            plant_type=plant_type,
            description=description,
            contact_info=contact_info,
            location_name=location_name,
            latitude=location.latitude,
            longitude=location.longitude,
            user_id=current_user.id
        )
        session.add(post)
        session.commit()

        return redirect(url_for('main.home'))

    return render_template('create_post.html')

    


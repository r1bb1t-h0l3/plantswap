from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from geopy.geocoders import Nominatim
from .models import Post, SessionLocal, User
from werkzeug.security import check_password_hash
from email_validator import validate_email, EmailNotValidError
import os

# Define a blueprint for routing
main = Blueprint('main', __name__)

@main.route('/', methods =['GET'])
def home():
    session = SessionLocal()
    location_filter = request.args.get('location')
    indoor_filter = request.args.get('is indoor')
    size_filter = request.args.get('size')
    flowering_filter = request.args.get('is_flowering')
    difficulty_filter = request.args.get('difficulty')
    sunlight_filter = request.args.get('sunlight')

    # Base query
    query = session.query(Post)

    #Dynamic filters
    if location_filter:
        query = query.filter(Post.location_name.ilike(f"%{location_filter}%"))
    if indoor_filter:
        query = query.filter(Post.is_indoor == (indoor_filter.lower() == 'true'))
    if size_filter:
        query = query.filter(Post.size.ilike(f"%{size_filter}%"))
    if flowering_filter:
        query = query.filter(Post.is_flowering == (flowering_filter.lower() == 'true'))
    if difficulty_filter:
        query = query.filter(Post.difficulty == (difficulty_filter.lower() == 'true'))
    if sunlight_filter:
        query = query.filter(Post.sunlight == (sunlight_filter.lower() == 'true'))
    
    posts = query.all()
    session.close()

    # Pass active filters to template for UI
    active_filters = {
        "location": location_filter,
        "is_indoor": indoor_filter,
        "size": size_filter,
        "is_flowering": flowering_filter,
        "difficulty": difficulty_filter,
        "sunlight": sunlight_filter
    }

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

    return render_template('index.html', message=message, posts=posts, map_data=map_data, active_filters=active_filters)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #  get form data
        username = request.form['username']
        password = request.form['password']
        
        session = SessionLocal()

        # look up if user by username
        # Look up the user by username
        user = session.query(User).filter_by(username=username).first()

        if user:
            # Verify the password
            if check_password_hash(user.password, password):
                # Log the user in
                login_user(user)
                flash('Login successful!', 'success')
                session.close()
                return redirect(url_for('main.home'))
            else:
                flash('Invalid username or password', 'danger')
        else:
            flash('Invalid username or password', 'danger')

        session.close()

        return redirect(url_for('main.home'))
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Email validation step
        try:
            valid = validate_email(email)
            email = valid.email # replace with normalised email if appropriate
        except EmailNotValidError as e:
            flash(str(e), 'danger')
            return redirect(url_for('main.register'))
        
        if not username or not email or not password or not confirm_password:
            flash('All fields required', 'danger')
            return redirect(url_for('main.register'))
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('main.register'))
        
        session = SessionLocal()

        #check if username or email already exists

        if session.query(User).filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            session.close()
            return redirect(url_for('main.register'))
        if session.query(User).filter_by(email=email).first():
            flash('Email already registered. Please use a different email.')
            session.close()
            return redirect(url_for('main.register'))

        # create new user
        new_user = User(
            username = username,
            email=email,
        )
        new_user.set_password(password) # hash password

        session.add(new_user)
        session.commit()
        session.close()

        flash('Registration successful! You can log in :)', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@main.route('/user', methods=['GET'])
@login_required
def user_domain():
    session = SessionLocal()
    
    user_posts = session.query(Post).filter_by(user_id=current_user.id).all()
    session.close()
    
    return render_template('user_domain.html', user_posts=user_posts)  

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))
    
@main.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    session = SessionLocal()

    if request.method == 'POST':
        plant_type = request.form.get('plantType')
        description = request.form.get('description')
        contact_info = request.form.get('contact')
        location_name = request.form.get('location')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        photo = request.files.get('photo')  # Handle file uploads if applicable

        # save uploaded photo
        photo_path = None
        if photo:
            photo_folder = 'app/static/upload'
            os.makedirs(photo_folder, exist_ok=True)
            photo_path = os.path.join(photo_folder, photo.filename)
            photo.save(photo_path)

        # create new post
        post = Post(
            plant_type=plant_type,
            description=description,
            contact_info=contact_info,
            location_name=location_name,
            latitude=float(latitude),
            longitude=float(longitude),
            photo=photo_path.replace('app/static/', '') if photo else None,
            user_id=current_user.id
        )

        session.add(post)
        session.commit()
        session.close()

        flash('Post created successfully!', 'success')
        return redirect(url_for('main.user_domain'))


@main.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query' '')

    if not query:
        return jsonify([])
    
    geolocator = Nominatim(user_agent="plantswap_app", timeout=5)
    try:
        locations = geolocator.geocode(query, exactly_one=False, limit=5)
    except GeopyError as e:
        return jsonify({"error": str(e)}), 500

    results = []
    if locations:
        for location in locations:
            results.append({
                "name": location.address,
                "latitude": location.latitude,
                "longitude": location.longitude
            })
    return jsonify(results)


    


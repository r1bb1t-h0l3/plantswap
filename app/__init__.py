from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base, User
import os 

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])


    # Database setup
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    Base.metadata.create_all(bind=engine)
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    # Initialize LoginManager with the app
    login_manager.init_app(app)

    # Set the login view (optional, if login required for some routes)
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    # Define the user_loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return SessionLocal().query(User).get(int(user_id))

    # Dependency Injection for session
    @app.teardown_appcontext
    def remove_session(exception=None):
        SessionLocal.remove()

    from .routes import main
    app.register_blueprint(main)

    return app

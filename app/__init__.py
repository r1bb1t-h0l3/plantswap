from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .models import User, SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base, User
from flask_migrate import Migrate
import os 

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath(os.path.join(os.getcwd(), 'site.db'))}"
    print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoid unnecessary overhead


    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Set up LoginManager options
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    # Define the user_loader callback
    @login_manager.user_loader
    def load_user(user_id):
        '''
        Manually query user usinng Session local because using declarative base'''
        session = SessionLocal()
        user = session.query(User).get(int(user_id))
        session.close()
        return user

    from .routes import main
    app.register_blueprint(main)

    return app

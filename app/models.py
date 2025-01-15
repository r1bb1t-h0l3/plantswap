from sqlalchemy import Column, Integer, String, create_engine, Text, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from flask_login import UserMixin

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    # Relationship to posts
    posts = relationship('Post', back_populates='author')

    @staticmethod
    def get(session, user_id):
        return session.query(User).get(user_id)
    
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    plant_type = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    contact_info = Column(String(150), nullable=False)
    photo = Column(String(150), nullable=True)  # Path to the photo file
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Location fields
    location_name = Column(String(150), nullable=False)  # City or neighborhood name
    latitude = Column(Float, nullable=False)  # Geographical latitude
    longitude = Column(Float, nullable=False)  # Geographical longitude

    author = relationship('User', back_populates='posts')

# Example of connecting to a database and creating a session
DATABASE_URL = "sqlite:///site.db"  # Replace with your actual database URL

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Create the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables (run this during initialization)
Base.metadata.create_all(bind=engine)

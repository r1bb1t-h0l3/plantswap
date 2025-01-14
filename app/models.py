from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from flask_login import UserMixin

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(150), nullable=False)

    @staticmethod
    def get(session, user_id):
        return session.query(User).get(user_id)

# Example of connecting to a database and creating a session
DATABASE_URL = "sqlite:///site.db"  # Replace with your actual database URL

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Create the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables (run this during initialization)
Base.metadata.create_all(bind=engine)

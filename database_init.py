from app.models import Base, engine

# Initialize the database
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created!")

from app import create_app, db
from app.models import User, Post, SessionLocal
from werkzeug.security import generate_password_hash

session = SessionLocal() # because using declarative base

# Add dummy users
user1 = User(
    username="Alice",
    email="alice@example.com",
    password=generate_password_hash("password1"),
)
user2 = User(
    username="Bob",
    email="bob@example.com",
    password=generate_password_hash("password2"),
)
user3 = User(
    username="Charlie",
    email="charlie@example.com",
    password=generate_password_hash("password3"),
)

session.add_all([user1, user2, user3])
session.commit()

# Add dummy posts
post1 = Post(
    plant_type="Cactus",
    description="A small but lively cactus for trade.",
    contact_info="alice@example.com",
    location_name="Mitte, Berlin",
    latitude=52.5200,
    longitude=13.4050,
    user_id=user1.id,
)
post2 = Post(
    plant_type="Succulent",
    description="Healthy succulent ready for a new home.",
    contact_info="bob@example.com",
    location_name="Neukölln, Berlin",
    latitude=52.4800,
    longitude=13.4376,
    user_id=user2.id,
)
post3 = Post(
    plant_type="Fern",
    description="Lush fern looking for a swap partner.",
    contact_info="charlie@example.com",
    location_name="Mitte, Berlin",
    latitude=52.5200,
    longitude=13.4100,
    user_id=user3.id,
)

session.add_all([post1, post2, post3])
session.commit()
session.close() # need to explicitly close session

print("Database populated successfully with dummy users and posts!")

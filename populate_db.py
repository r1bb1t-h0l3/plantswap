from app.models import SessionLocal, User, Post

# Start a new session
session = SessionLocal()

# Create dummy users
user1 = User(username="johndoe", email="johndoe@example.com", password="hashed_password")
user2 = User(username="janedoe", email="janedoe@example.com", password="hashed_password")

session.add_all([user1, user2])
session.commit()

# Create dummy posts
post1 = Post(
    plant_type="Cactus",
    description="A beautiful cactus looking for a new home.",
    contact_info="johndoe@example.com",
    location_name="Berlin, Germany",
    latitude=52.5200,
    longitude=13.4050,
    user_id=user1.id
)

post2 = Post(
    plant_type="Succulent",
    description="Healthy succulent available for swap.",
    contact_info="janedoe@example.com",
    location_name="Munich, Germany",
    latitude=48.1351,
    longitude=11.5820,
    user_id=user2.id
)

session.add_all([post1, post2])
session.commit()

print("Database populated with dummy posts!")
session.close()

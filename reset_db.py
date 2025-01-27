from app.models import SessionLocal, Post, User

def reset_database():
    session = SessionLocal()
    # Delete all posts and users
    session.query(Post).delete()
    session.query(User).delete()
    session.commit()
    session.close()
    print("Database reset successfully!")

if __name__ == "__main__":
    reset_database()

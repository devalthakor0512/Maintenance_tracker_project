from app.database import SessionLocal
from app.models.user import User

def promote_users_to_admin():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"Found {len(users)} users.")
        for user in users:
            print(f"Promoting user {user.email} from '{user.role}' to 'admin'...")
            user.role = "admin"
        
        db.commit()
        print("All users promoted to admin successfully!")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    promote_users_to_admin()

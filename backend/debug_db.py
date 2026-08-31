from app.database import SessionLocal, engine, Base
from app.models import user as models
from app.utils import helpers

def test_db_insert():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("Hashing password...")
        pwd = "Password123!"
        hashed = helpers.get_password_hash(pwd)
        print(f"Hashed: {hashed}")

        print("Creating user...")
        new_user = models.User(
            email="debug@example.com",
            hashed_password=hashed,
            full_name="Debug User",
            role="portal_user"
        )
        db.add(new_user)
        print("Committing...")
        db.commit()
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_db_insert()

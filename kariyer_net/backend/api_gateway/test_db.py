from app.core.database import SessionLocal
from app.models.user import User

try:
    db = SessionLocal()
    # Try to query the users table
    users = db.query(User).all()
    print(f"Database connection successful! Found {len(users)} users.")
    db.close()
except Exception as e:
    print(f"Database connection error: {e}") 
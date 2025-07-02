from app.core.database import engine, Base
from app.models.user import User

# Drop all tables
Base.metadata.drop_all(bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

print("Database tables dropped and recreated successfully!") 
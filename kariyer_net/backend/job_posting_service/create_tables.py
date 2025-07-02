from app.core.database import Base, engine
from app.models.job import Job
from app.models.application import JobApplication
from app.models.company import Company
# Add other models as needed
 
if __name__ == "__main__":
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.") 
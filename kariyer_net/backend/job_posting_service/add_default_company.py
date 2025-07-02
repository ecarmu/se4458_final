from app.core.database import SessionLocal
from app.models.company import Company

def add_default_company():
    db = SessionLocal()
    try:
        # Check if default company already exists
        existing_company = db.query(Company).filter(Company.id == 1).first()
        if not existing_company:
            # Create default company
            default_company = Company(
                id=1,
                name="Default Company",
                logo_url="",
                location="Istanbul, Turkey",
                jobs="[]"
            )
            db.add(default_company)
            db.commit()
            print("Default company created successfully!")
        else:
            print("Default company already exists.")
    except Exception as e:
        print(f"Error creating default company: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_default_company() 
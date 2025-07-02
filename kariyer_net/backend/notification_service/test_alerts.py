import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.alert import JobAlert
from app.core.database import Base
from datetime import datetime

def get_test_db():
    db_fd, db_path = tempfile.mkstemp()
    engine = create_engine(f"sqlite:///{db_path}")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        os.close(db_fd)
        os.unlink(db_path)

def run_create_alert_test():
    for db in get_test_db():
        alert = JobAlert(
            user_id=123,
            job_name="Python Developer",
            location="Istanbul",
            employment_type="full-time",
            is_active=True,
            frequency="daily"
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        try:
            assert alert.id is not None, "id is None"
            assert alert.created_at is not None, "created_at is None"
            assert alert.frequency == "daily", f"frequency is {alert.frequency}"
            assert alert.location == "Istanbul", f"location is {alert.location}"
            assert alert.job_name == "Python Developer", f"job_name is {alert.job_name}"
            assert alert.is_active is True, f"is_active is {alert.is_active}"
            print("PASS: Alert creation test succeeded.")
        except AssertionError as e:
            print(f"FAIL: {e}")

if __name__ == "__main__":
    run_create_alert_test() 
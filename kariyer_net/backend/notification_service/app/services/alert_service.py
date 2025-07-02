from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.alert import JobAlert
from ..schemas.alert import AlertCreate
from ..core.database import get_db

class AlertService:
    def __init__(self, db: Session):
        self.db = db

    async def create_alert(self, alert: AlertCreate) -> JobAlert:
        """Create a new job alert"""
        if not alert.query or not alert.location:
            raise ValueError("Both 'query' and 'location' must be provided.")
        db_alert = JobAlert(
            user_id=alert.user_id,
            job_name=alert.query,
            location=alert.location,
            employment_type=None,  # Extend as needed
            is_active=True,
            frequency=alert.frequency
        )
        self.db.add(db_alert)
        self.db.commit()
        self.db.refresh(db_alert)
        return db_alert

    async def get_user_alerts(self, user_id: int) -> List[JobAlert]:
        """Get user's job alerts"""
        return self.db.query(JobAlert).filter(JobAlert.user_id == user_id).all()

    async def update_alert(self, alert_id: int, alert_data: dict) -> Optional[JobAlert]:
        """Update an alert"""
        # To be implemented
        pass

    async def delete_alert(self, alert_id: int) -> bool:
        """Delete an alert"""
        # To be implemented
        pass

    def get_all_active_alerts(self) -> List[JobAlert]:
        """Get all active job alerts"""
        return self.db.query(JobAlert).filter(JobAlert.is_active == True).all() 
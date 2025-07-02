from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....schemas.alert import AlertCreate, AlertResponse
from ....services.alert_service import AlertService

router = APIRouter()

def get_alert_service(db: Session = Depends(get_db)) -> AlertService:
    return AlertService(db)

@router.post("/", response_model=AlertResponse)
async def create_job_alert(
    alert: AlertCreate,
    alert_service: AlertService = Depends(get_alert_service)
):
    db_alert = await alert_service.create_alert(alert)
    # Ensure query is a string and keywords is present
    response = db_alert.__dict__.copy()
    response['query'] = response.get('job_name') or ""
    response['keywords'] = [response['query']] if response['query'] else []
    return response

@router.get("/", response_model=List[AlertResponse])
async def get_user_alerts(
    user_id: int,
    alert_service: AlertService = Depends(get_alert_service)
):
    db_alerts = await alert_service.get_user_alerts(user_id)
    responses = []
    for db_alert in db_alerts:
        resp = db_alert.__dict__.copy()
        resp['query'] = resp.get('job_name') or ""
        resp['keywords'] = [resp['query']] if resp['query'] else []
        responses.append(resp)
    return responses
# app/api/log_routes.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.log_schema import LogCreate
from app.models.log_model import Log
from app.core.database import get_db
from datetime import datetime

router = APIRouter()

@router.post("/logs")
def create_log(log: LogCreate, db: Session = Depends(get_db)):
    try:
        new_log = Log(
            username=log.username,
            ip_address=str(log.ip_address),
            action=log.action,
            result=log.result,
            endpoint=log.endpoint,
            timestamp=datetime.utcnow()
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return {"message": "Log created successfully", "log_id": new_log.id}

    except Exception as e:
        print("🔥 ERROR WHILE SAVING LOG:", e)  # 👈 add this
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
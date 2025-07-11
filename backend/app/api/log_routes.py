# app/api/log_routes.py
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.log_schema import LogCreate
from app.schemas.log_schema import LogResponse
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

@router.post("/logs/bulk")
def create_logs_bulk(logs: List[LogCreate], db: Session = Depends(get_db)):
    try:
        new_logs = [
            Log(
                username=log.username,
                ip_address=str(log.ip_address),
                action=log.action,
                result=log.result,
                endpoint=log.endpoint,
                timestamp=datetime.utcnow()
            )
            for log in logs
        ]
        db.add_all(new_logs)
        db.commit()
        return {"message": f"{len(new_logs)} logs inserted successfully"}

    except Exception as e:
        db.rollback()
        print("🔥 BULK INSERT ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to insert logs")

@router.get("/logs", response_model=List[LogResponse])
def get_logs(
    skip: int = 0,
    limit: int = 100,
    username: str = Query(None),
    action: str = Query(None),
    result: str = Query(None),
    sort: str = Query("desc"),  # "asc" or "desc"
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Log)

    if username:
        query = query.filter(Log.username == username)
    if action:
        query = query.filter(Log.action == action)
    if result:
        query = query.filter(Log.result == result)
    if start_date:
        query = query.filter(Log.timestamp >= start_date)
    if end_date:
        query = query.filter(Log.timestamp <= end_date)

    if sort == "asc":
        query = query.order_by(Log.timestamp.asc())
    else:
        query = query.order_by(Log.timestamp.desc())

    logs = query.offset(skip).limit(limit).all()
    return logs

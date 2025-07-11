# app/schemas/log_schema.py

from pydantic import BaseModel, IPvAnyAddress
from typing import Optional
from datetime import datetime

class LogCreate(BaseModel):
    username: str
    ip_address: IPvAnyAddress
    action: str
    result: str
    endpoint: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "hassan_98",
                "ip_address": "192.168.1.15",
                "action": "login",
                "result": "failed",
                "endpoint": "/login"
            }
        }

class LogResponse(LogCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import request as models
from ..models import equipment as equipment_models
from ..schemas import request as schemas
from ..utils.dependencies import get_current_user
from ..models.user import User

router = APIRouter(
    prefix="/requests",
    tags=["Maintenance Requests"]
)

@router.get("/", response_model=List[schemas.RequestResponse])
def read_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    requests = db.query(models.Request).offset(skip).limit(limit).all()
    return requests

@router.post("/", response_model=schemas.RequestResponse)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Fetch Equipment
    equipment = db.query(equipment_models.Equipment).filter(equipment_models.Equipment.id == request.equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    # 2. Smart Auto-fill Logic
    # Extract data from equipment to fill request
    auto_category = equipment.category
    auto_team_id = equipment.maintenance_team_id

    # 3. Create Request
    new_request = models.Request(
        subject=request.subject,
        equipment_id=request.equipment_id,
        request_type=request.request_type,
        scheduled_date=request.scheduled_date,
        duration=request.duration,
        stage=request.stage,
        assigned_technician_id=request.assigned_technician_id,
        # Auto-filled
        category=auto_category,
        maintenance_team_id=auto_team_id
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@router.delete("/{request_id}")
def delete_request(request_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    
    db.delete(request)
    db.commit()
    return {"message": "Request deleted"}

@router.put("/{request_id}", response_model=schemas.RequestResponse)
def update_request(request_id: int, request_update: schemas.RequestUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    # Update fields
    for key, value in request_update.model_dump(exclude_unset=True).items():
        setattr(request, key, value)

    db.commit()
    db.refresh(request)
    return request

@router.get("/calendar", response_model=List[schemas.RequestResponse])
def get_calendar_requests(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Simple example to filter for Preventive maintenance which usually has dates
    requests = db.query(models.Request).filter(models.Request.request_type == "Preventive").all()
    return requests

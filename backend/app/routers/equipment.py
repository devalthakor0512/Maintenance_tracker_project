from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import equipment as models
from ..models import request as request_models
from ..schemas import equipment as schemas
from ..schemas import request as request_schemas
from ..utils.dependencies import get_current_user, get_current_admin_user
from ..models.user import User

router = APIRouter(
    prefix="/equipment",
    tags=["Equipment"]
)

@router.get("/", response_model=List[schemas.EquipmentResponse])
def read_equipment(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    equipment = db.query(models.Equipment).offset(skip).limit(limit).all()
    return equipment

@router.get("/{equipment_id}", response_model=schemas.EquipmentResponse)
def read_equipment_by_id(equipment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    equipment = db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.get("/{equipment_id}/requests", response_model=List[request_schemas.RequestResponse])
def read_equipment_requests(equipment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    equipment = db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    if equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment.requests

@router.post("/", response_model=schemas.EquipmentResponse)
def create_equipment(equipment: schemas.EquipmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_equipment = db.query(models.Equipment).filter(models.Equipment.serial_number == equipment.serial_number).first()
    if db_equipment:
        raise HTTPException(status_code=400, detail="Equipment with this Serial Number already exists")
    
    new_equipment = models.Equipment(**equipment.model_dump())
    db.add(new_equipment)
    db.commit()
    db.refresh(new_equipment)
    return new_equipment

@router.put("/{equipment_id}", response_model=schemas.EquipmentResponse)
def update_equipment(equipment_id: int, equipment_update: schemas.EquipmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_equipment = db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    if not db_equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    for key, value in equipment_update.model_dump().items():
        setattr(db_equipment, key, value)
    
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

@router.delete("/{equipment_id}")
def delete_equipment(equipment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    db_equipment = db.query(models.Equipment).filter(models.Equipment.id == equipment_id).first()
    if not db_equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    db.delete(db_equipment)
    db.commit()
    return {"message": "Equipment deleted"}

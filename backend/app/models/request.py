from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from ..database import Base

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    request_type = Column(String) # "Corrective" or "Preventive"
    scheduled_date = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True) # hours spent
    stage = Column(String, default="New") # "New", "In Progress", "Repaired", "Scrap"
    
    # Auto-filled fields (as per requirement logic, stored for historical accuracy)
    category = Column(String, nullable=True)
    maintenance_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    assigned_technician_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())

    equipment = relationship("Equipment", back_populates="requests")
    technician = relationship("User", foreign_keys=[assigned_technician_id], backref="assigned_requests")
    team = relationship("Team") 

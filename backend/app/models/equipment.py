from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    equipment_name = Column(String, index=True)
    serial_number = Column(String, unique=True, index=True)
    category = Column(String) # "Computer", "Vehicle", etc.
    department = Column(String)
    location = Column(String)
    purchase_date = Column(Date, nullable=True)
    warranty_expiry = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String, default="active") # "active", "maintenance", "scrapped"

    assigned_employee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    maintenance_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    assigned_to = relationship("User", foreign_keys=[assigned_employee_id], backref="assigned_equipment")
    team = relationship("Team", backref="equipment_list")
    requests = relationship("Request", back_populates="equipment")

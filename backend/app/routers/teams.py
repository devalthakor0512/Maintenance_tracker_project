from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from ..database import get_db
from ..models import team as models
from ..schemas import team as schemas
from ..models import user as user_models
from ..utils.dependencies import get_current_user, get_current_admin_user

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)

@router.get("/", response_model=List[schemas.TeamResponse])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: user_models.User = Depends(get_current_user)):
    teams = db.query(models.Team).options(joinedload(models.Team.members)).offset(skip).limit(limit).all()
    return teams

@router.post("/", response_model=schemas.TeamResponse)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db), current_user: user_models.User = Depends(get_current_admin_user)):
    db_team = db.query(models.Team).filter(models.Team.team_name == team.team_name).first()
    if db_team:
        raise HTTPException(status_code=400, detail="Team already exists")
    
    new_team = models.Team(team_name=team.team_name)
    db.add(new_team)
    
    # Add members
    if team.members:
        users = db.query(user_models.User).filter(user_models.User.id.in_(team.members)).all()
        new_team.members = users # SQLAlchemy detects this change on the tracked object

    db.commit()
    db.refresh(new_team)
    return new_team

@router.put("/{team_id}", response_model=schemas.TeamResponse)
def update_team(team_id: int, team_update: schemas.TeamCreate, db: Session = Depends(get_db), current_user: user_models.User = Depends(get_current_admin_user)):
    team_query = db.query(models.Team).filter(models.Team.id == team_id)
    team = team_query.options(joinedload(models.Team.members)).first()
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    team.team_name = team_update.team_name
    
    # Update members
    if team_update.members is not None:
        users = db.query(user_models.User).filter(user_models.User.id.in_(team_update.members)).all()
        team.members = users
        
    db.commit()
    db.refresh(team)
    return team

@router.delete("/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db), current_user: user_models.User = Depends(get_current_admin_user)):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db.delete(team)
    db.commit()
    return {"message": "Team deleted"}

@router.post("/{team_id}/members/{user_id}", response_model=schemas.TeamResponse)
def add_member_to_team(team_id: int, user_id: int, db: Session = Depends(get_db), current_user: user_models.User = Depends(get_current_admin_user)):
    team = db.query(models.Team).options(joinedload(models.Team.members)).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    user = db.query(user_models.User).filter(user_models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user not in team.members:
        team.members.append(user)
        db.commit()
        db.refresh(team)
    return team

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import user as models
from ..schemas import user as schemas
from ..utils import helpers
from datetime import timedelta
from ..config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Router for user management (fetching lists etc)
users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Account already exists")

    # Validate password strength
    helpers.validate_password_strength(user.password)

    # Create new user
    hashed_password = helpers.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role="portal_user" # Explicitly set as per requirement
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    # Check for Login Credentials
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if not user:
        # If email not found then throw error "Account not exist"
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not exist"
        )
    
    # Password does not match -> error msg "Invalid Password"
    if not helpers.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, # Or 401
            detail="Invalid Password"
        )
    
    # Generate Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = helpers.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

from typing import List
from ..utils.dependencies import get_current_user
from ..models.user import User

@users_router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # In a real app, restrict to Admin only or filter fields
    return db.query(models.User).all()

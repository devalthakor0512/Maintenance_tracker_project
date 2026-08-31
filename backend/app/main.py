from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import users, teams, equipment, requests
from .models import user, team, equipment as equip_model, request as req_model # Import all models to ensure create_all sees them

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Maintenance Tracker API")

# CORS Middleware
origins = [
    "http://localhost:5500", # Access from frontend (e.g. Next.js / React)
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(users.users_router)
app.include_router(teams.router)
app.include_router(equipment.router)
app.include_router(requests.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Maintenance Tracker API"}

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.utils.helpers import get_password_hash

# Ensure tables exist
# Base.metadata.create_all(bind=engine)

db = SessionLocal()

technicians = [
    ("Aarav Sharma", "IT Support Technician"),
    ("Riya Banerjee", "Network & Systems Technician"),
    ("Rohan Mehta", "Mechanical Maintenance Technician"),
    ("Mohit Saxena", "Heavy Machinery Technician"),
    ("Aditya Verma", "Electrical Maintenance Technician"),
    ("Sneha Iyer", "Industrial Electrician"),
    ("Arjun Singh", "CNC Machine Operator & Maintenance"),
    ("Kunal Jain", "Production Equipment Technician"),
    ("Rahul Khanna", "Vehicle Maintenance Technician"),
    ("Varun Kapoor", "Fleet & Transport Technician"),
    ("Priya Shah", "Printer & Office Hardware Technician"),
    ("Aman Bansal", "Desktop & Peripheral Technician"),
    ("Shreya Kulkarni", "Quality Control Technician"),
    ("Nidhi Chawla", "Equipment Inspection Technician"),
    ("Siddharth Malhotra", "Multi-Skill Maintenance Technician"),
    ("Neha Agarwal", "Facility Maintenance Technician"),
    ("Pooja Joshi", "HVAC & Cooling Systems Technician"),
    ("Sanjay Patel", "Utilities & Power Systems Technician"),
    ("Ankit Desai", "Safety & Compliance Technician"),
    ("Mehul Trivedi", "Preventive Maintenance Specialist")
]

default_password_hash = get_password_hash("GearGuard@2025")

print("Seeding technicians...")

# Optional: Clear existing non-admin users to clean up list?
# Be careful not to delete the user's current account if they are logged in as admin.
# For now, let's just add the new ones.

count = 0
for name, title in technicians:
    email = f"{name.lower().replace(' ', '.')}@gearguard.com"
    email = email.replace("&", "and") # Sanitize
    
    # Check if exists
    existing = db.query(User).filter(User.email == email).first()
    if not existing:
        user = User(
            email=email,
            full_name=name,
            hashed_password=default_password_hash,
            role=title
        )
        db.add(user)
        count += 1
        print(f"Added: {name} ({title})")
    else:
        # Update role if exists
        if existing.role != title:
            existing.role = title
            existing.full_name = name
            print(f"Updated: {name}")

db.commit()
print(f"Detailed seeding complete. Added {count} new technicians.")
db.close()

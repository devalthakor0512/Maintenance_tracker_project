import requests
import sys
from sqlalchemy import create_engine, text
from app.config import settings

BASE_URL = 'http://127.0.0.1:8000'

DB_URL = settings.DATABASE_URL

def promote_to_admin(email):
    # Direct DB Hack for testing
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        conn.execute(text(f"UPDATE users SET role='admin' WHERE email='{email}'"))
        conn.commit()
    print(f"👑 Promoted {email} to admin")

def test_full_flow():
    # 1. Signup Admin
    admin_data = {"email": "krithik@example.com", "password": "AdminPassword123!", "full_name": "Admin User"}
    requests.post(f"{BASE_URL}/auth/signup", json=admin_data) # Ignore error if exists
    promote_to_admin(admin_data["email"])
    
    # Login Admin
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": admin_data["email"], "password": admin_data["password"]})
    if resp.status_code != 200:
        print("❌ Admin Login Failed")
        return
    admin_token = resp.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("✅ Admin Logged In")

    # 2. Create Team
    team_data = {"team_name": "Rapid Response Team"}
    resp = requests.post(f"{BASE_URL}/teams/", json=team_data, headers=admin_headers)
    if resp.status_code == 200:
        team_id = resp.json()["id"]
        print(f"✅ Team Created: {team_id}")
    elif resp.status_code == 400: # Already exists
        # Get existing team
        all_teams = requests.get(f"{BASE_URL}/teams/", headers=admin_headers).json()
        team_id = next(t["id"] for t in all_teams if t["team_name"] == team_data["team_name"])
        print(f"ℹ️ Team Existed: {team_id}")
    else:
        print(f"❌ Create Team Failed: {resp.text}")
        return

    # 3. Create Equipment
    equip_data = {
        "equipment_name": "Hydraulic Press",
        "serial_number": "HP-9000",
        "category": "Heavy Machinery",
        "department": "Assembly",
        "location": "Sector 7",
        "maintenance_team_id": team_id 
    }
    resp = requests.post(f"{BASE_URL}/equipment/", json=equip_data, headers=admin_headers)
    if resp.status_code == 200:
        equip_id = resp.json()["id"]
        print(f"✅ Equipment Created: {equip_id}")
    elif resp.status_code == 400:
        all_equip = requests.get(f"{BASE_URL}/equipment/", headers=admin_headers).json()
        equip_id = next(e["id"] for e in all_equip if e["serial_number"] == equip_data["serial_number"])
        print(f"ℹ️ Equipment Existed: {equip_id}")
    else:
        print(f"❌ Create Equipment Failed: {resp.text}")
        return

    # 4. Signup User (Normal)
    user_data = {"email": "worker@example.com", "password": "WorkerPassword123!", "full_name": "Worker Bee"}
    requests.post(f"{BASE_URL}/auth/signup", json=user_data)
    
    # Login User
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": user_data["email"], "password": user_data["password"]})
    user_token = resp.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}
    print("✅ User Logged In")

    # 5. Create Request (Verify Auto-fill)
    req_data = {
        "subject": "Press not pressing",
        "equipment_id": equip_id,
        "request_type": "Corrective"
    }
    resp = requests.post(f"{BASE_URL}/requests/", json=req_data, headers=user_headers)
    if resp.status_code == 200:
        req_json = resp.json()
        print("✅ Request Created")
        
        # Verify Auto-fill
        if req_json["category"] == "Heavy Machinery" and req_json["maintenance_team_id"] == team_id:
            print("✨ Auto-fill Verified: Category & Team ID matched equipment!")
        else:
            print(f"❌ Auto-fill Failed values: {req_json}")
    else:
        print(f"❌ Create Request Failed: {resp.text}")

if __name__ == "__main__":
    try:
        test_full_flow()
    except Exception as e:
        print(f"Error: {e}")

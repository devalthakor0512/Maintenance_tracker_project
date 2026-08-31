import requests

BASE_URL = "http://127.0.0.1:8000"

def test_rbac():
    print("Testing RBAC...")
    # 1. Login as User (Worker)
    # Assuming verify_full_flow.py ran, duplicate signup might fail, so login
    user_cred = {"email": "worker@example.com", "password": "WorkerPassword123!"}
    resp = requests.post(f"{BASE_URL}/auth/login", json=user_cred)
    token = resp.json().get("access_token")
    if not token:
        # Try signing up if not exists
         requests.post(f"{BASE_URL}/auth/signup", json={**user_cred, "full_name": "Worker"})
         resp = requests.post(f"{BASE_URL}/auth/login", json=user_cred)
         token = resp.json().get("access_token")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Try Create Equipment as User
    equip_data = {
        "equipment_name": "Unauthorized Press",
        "serial_number": "NO-ACCESS-1",
        "category": "Restricted",
        "department": "Secret",
        "location": "Nowhere"
    }
    resp = requests.post(f"{BASE_URL}/equipment/", json=equip_data, headers=headers)
    if resp.status_code == 403:
        print("✅ RBAC Success: User cannot create Equipment (403 Forbidden)")
    else:
        print(f"❌ RBAC Failed: User got {resp.status_code} - {resp.text}")

    # 3. Try Create Team as User
    team_data = {"team_name": "Hacker Team"}
    resp = requests.post(f"{BASE_URL}/teams/", json=team_data, headers=headers)
    if resp.status_code == 403:
        print("✅ RBAC Success: User cannot create Team (403 Forbidden)")
    else:
        print(f"❌ RBAC Failed: User got {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    test_rbac()

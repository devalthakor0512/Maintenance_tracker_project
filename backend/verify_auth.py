import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_signup():
    print("Testing Signup...")
    # 1. Successful Signup
    payload = {
        "email": "test@example.com",
        "password": "Password123!",
        "full_name": "Anubug"
    }
    response = requests.post(f"{BASE_URL}/auth/signup", json=payload)
    if response.status_code == 200:
        print("✅ Signup Success")
    else:
        print(f"❌ Signup Failed: {response.text}")

    # 2. Duplicate Signup
    response = requests.post(f"{BASE_URL}/auth/signup", json=payload)
    if response.status_code == 400 and "Account already exists" in response.text:
        print("✅ Duplicate Check Success")
    else:
        print(f"❌ Duplicate Check Failed: {response.status_code} {response.text}")

    # 3. Weak Password
    weak_payload = {
        "email": "weak@example.com",
        "password": "weak",
        "full_name": "Weak User"
    }
    response = requests.post(f"{BASE_URL}/auth/signup", json=weak_payload)
    if response.status_code == 400:
        print("✅ Weak Password Check Success")
    else:
        print(f"❌ Weak Password Check Failed: {response.status_code} {response.text}")

def test_login():
    print("\nTesting Login...")
    # 1. Successful Login
    payload = {
        "email": "test@example.com",
        "password": "Password123!"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    if response.status_code == 200:
        print("✅ Login Success")
        token = response.json().get("access_token")
        if token:
            print("✅ Token Received")
        else:
            print("❌ No Token in Response")
    else:
        print(f"❌ Login Failed: {response.text}")

    # 2. Invalid Password
    bad_payload = {
        "email": "test@example.com",
        "password": "WrongPassword123!"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=bad_payload)
    if response.status_code == 400 and "Invalid Password" in response.text:
        print("✅ Invalid Password Check Success") # Code handles 400 or 401, I set 400 in implementation
    elif response.status_code == 401: # Check if I changed it
         print("✅ Invalid Password Check Success (401)")
    else:
        print(f"❌ Invalid Password Check Failed: {response.status_code} {response.text}")

    # 3. non-existent Account
    no_user_payload = {
        "email": "nobody@example.com",
        "password": "Password123!"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=no_user_payload)
    if response.status_code == 404 and "Account not exist" in response.text:
        print("✅ Non-existent Account Check Success")
    else:
        print(f"❌ Non-existent Account Check Failed: {response.status_code} {response.text}")

if __name__ == "__main__":
    try:
        test_signup()
        test_login()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is it running?")

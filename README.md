# 🛡️ GearGuard - Maintenance Tracker System

> A modern, robust, and full-stack solution for managing industrial equipment maintenance, teams, and service requests.

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)

---

## 🔍 Overview

**GearGuard** is designed to streamline the workflow of maintenance departments. It serves as a central hub for tracking machinery, assigning maintenance teams, scheduling repairs, and monitoring operational status in real-time.

Built with a performance-first mindset using **FastAPI** for the backend and a lightweight, visually stunning **Vanilla JS** frontend with 3D elements.

---

## ✨ Key Features

### 🚀 **Dashboard & Analytics**
- Real-time overview of **Total Equipment**, **Active Requests**, and **Team Availability**.
- Visual indicators for system health and uptime.

### 🏭 **Equipment Management**
- **Asset Tracking**: Catalog all machinery with serial numbers, categories, and locations.
- **Status Monitoring**: Track if equipment is Operational, Under Maintenance, or Retired.
- **Auto-fill**: Smart integration with requests to auto-populate category and team details.

### 👥 **Team & Technician Hub**
- **Team Management**: Create specialized groups (e.g., "Electrical Team", "Heavy Machinery").
- **Technician Database**: Seedable database of skilled technicians.
- **Member Assignment**: Dynamic assignment of technicians to teams.

### 🎫 **Request System (Kanban Board)**
- **Workflow Visualization**: Drag-and-drop Kanban board for managing request lifecycle (`New` -> `In Progress` -> `Repaired` -> `Scrap`).
- **Flexible Views**: Switch between **Kanban** and **List** views.
- **Prioritization**: Distinction between **Corrective** (Emergency) and **Preventive** maintenance.

### 📅 **Scheduler**
- **Maintenance Calendar**: Visual monthly calendar for scheduled maintenance.
- **Upcoming Alerts**: Sidebar widget for imminent service tasks.

### 🔐 **Security & Auth**
- **JWT Authentication**: Secure login sessions.
- **RBAC**: Role-Based Access Control (Admin/User).
- **Argon2 Hashing**: Industry-standard password security.

---

## 🛠 Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| **Backend** | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi) | High-performance API framework (Python) |
| **Database** | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite) | Lightweight, serverless DB (via SQLAlchemy) |
| **Frontend** | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5) ![JS](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript) | Native web technologies (No framework overhead) |
| **Styling** | ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3) | Custom dark-themed CSS with Glassmorphism |
| **3D Graphics** | **Spline** | Interactive 3D background elements |
| **Package Mgr** | ![uv](https://img.shields.io/badge/uv-purple?style=flat) | Blazing fast Python package installer |

---

## 📂 Project Structure

```bash
Odaoo project/
├── 📂 backend
│   ├── 📂 app
│   │   ├── 📂 models       # Database models (User, Team, Equipment, Request)
│   │   ├── 📂 routers      # API Endpoints
│   │   ├── 📂 schemas      # Pydantic data validation schemas
│   │   ├── database.py     # DB Connection
│   │   └── main.py         # Entry point
│   ├── seed_technicians.py # Script to populate dummy data
│   └── requirements.txt    # Python dependencies
│
└── 📂 frontend
    ├── 📂 js
    │   └── config.js       # API Base URL & Auth helpers
    ├── index.html          # Dashboard
    ├── login.html          # Auth Page
    ├── equipment.html      # Asset Management
    ├── teams.html          # Team Management
    ├── request.html        # Kanban Board
    └── calendar.html       # Schedule View
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+** installed.
- **Modern Web Browser** (Chrome/Edge/Firefox).
- *(Optional)* **VS Code** with "Live Server" extension.

### Backend Setup

1.  **Navigate to the backend folder:**
    ```powershell
    cd backend
    ```

2.  **Install Dependencies (using `uv` or `pip`):**
    ```powershell
    # Recommended (Faster)
    uv pip install -r requirements.txt
    
    # OR Standard
    pip install -r requirements.txt
    ```

3.  **Start the Server:**
    ```powershell
    uv run uvicorn app.main:app --reload
    ```
    > The API will start at `http://127.0.0.1:8000`. DB tables will be created automatically.

4.  **(Optional) Seed Initial Data:**
    Populate the database with a list of skilled technicians.
    ```powershell
    uv run python seed_technicians.py
    ```

### Frontend Setup

1.  **Navigate to the frontend folder:**
    ```powershell
    cd ../frontend
    ```

2.  **Run the App:**
    You can simply double-click `index.html` (though some features require a server) OR typically use a local development server like **Live Server**:
    
    *   **VS Code**: Right-click `index.html` -> **"Open with Live Server"**.
    *   **Python**: `python -m http.server 5500`

3.  **Access the Dashboard:**
    Open `http://127.0.0.1:5500` in your browser.

---

## 🎮 Usage Guide

1.  **Sign Up / Login**: Creates an account via the UI.
    *   *Note*: By default, new users have "portal_user" role.
    *   **Admin Access**: Run the `fix_admin_role.py` script in the backend to promote yourself to Admin capabilities:
        ```powershell
        uv run python fix_admin_role.py
        ```
2.  **Add Equipment**: Go to the **Equipment** tab to add new machinery.
3.  **Form Teams**: Go to **Teams**, click "Add Team", and select technicians from the list.
4.  **Create Requests**: Go to **Requests**, click "New Request". Select equipment (Category/Team will auto-fill).
5.  **Manage Workflow**: Drag cards on the Kanban board to update their status.

---

## 📡 API Documentation

Once the backend is running, you can access the interactive API docs (Swagger UI) to test endpoints directly.

👉 **URL**: `http://127.0.0.1:8000/docs`

---



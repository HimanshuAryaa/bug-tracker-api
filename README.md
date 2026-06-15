# 🐞 Bug Tracker

A full-stack bug tracking application built for organisations with role-based access control and JWT authentication. Users are assigned specific roles and can only perform actions permitted for their role.

> **Live API:** https://bug-tracker-api-kwyv.onrender.com

---

## 📁 Project Structure

```
bug-tracker-api/
├── app.py                        # App entry point, config, blueprints
├── models.py                     # Database models (User, Project, Bug)
├── extensions.py                 # db and bcrypt instances
├── routes/
│   ├── auth.py                   # Register, login, user management
│   ├── projects.py               # Project CRUD
│   └── bugs.py                   # Bug CRUD
├── bug-tracker-frontend/
│   ├── index.html                # Login page
│   ├── register.html             # Registration page
│   ├── dashboard.html            # Projects dashboard
│   └── bugs.html                 # Bug listing per project
├── requirements.txt
├── Procfile
└── README.md
```

---

## ✨ Features

### Backend
- User registration and login with bcrypt password hashing
- JWT token authentication
- Role-based access control — 4 roles with specific permissions
- Full CRUD for Projects and Bugs
- Bugs automatically linked to project's assigned developer on creation
- Reporter and assignee tracked on each bug
- CORS enabled for frontend integration

### Frontend
- Login and registration with client-side form validation
- Role-based UI — buttons and actions shown/hidden based on logged-in role
- Projects dashboard — view, add, edit, delete projects
- Per-project bug listing — view, add, edit, delete bugs
- Bug detail modal — view mode and edit mode
- 9 bug statuses with unique color indicators
- Severity and priority color-coded badges
- Responsive modern UI

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| Python | Core language |
| Flask | Web framework |
| PostgreSQL | Production database |
| SQLAlchemy | ORM |
| Flask-JWT-Extended | JWT authentication |
| Flask-Bcrypt | Password hashing |
| Flask-CORS | Cross-origin requests |

### Frontend
| Technology | Purpose |
|---|---|
| HTML | Structure |
| CSS | Styling |
| JavaScript (Vanilla) | Logic and API calls |

### Deployment
| Service | Usage |
|---|---|
| Render | Backend hosting |
| Render | PostgreSQL database |

---

## 👥 Roles & Permissions

| Permission | admin | manager | tester | developer |
|---|---|---|---|---|
| View all users | ✅ | ✅ | ❌ | ❌ |
| Delete user | ✅ | ❌ | ❌ | ❌ |
| Create project | ✅ | ✅ | ❌ | ❌ |
| View projects | ✅ | ✅ | ✅ (assigned only) | ✅ (assigned only) |
| Update project | ✅ | ✅ (own projects) | ❌ | ❌ |
| Delete project | ✅ | ✅ (own projects) | ❌ | ❌ |
| Report bug | ✅ | ❌ | ✅ (assigned project) | ❌ |
| Update bug title/severity/priority | ✅ | ❌ | ✅ (assigned project) | ❌ |
| Update bug status | ✅ | ❌ | ✅ (assigned project) | ✅ (assigned project) |
| View bugs | ✅ | ✅ | ✅ | ✅ |
| Delete bug | ✅ | ❌ | ❌ | ❌ |

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.8+
- PostgreSQL database (or update `DATABASE_URL` to use SQLite for local dev)

### Steps

1. Clone the repository
   ```bash
   git clone https://github.com/HimanshuAryaa/bug-tracker-api.git
   cd bug-tracker-api
   ```

2. Create and activate virtual environment
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Mac/Linux
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables

   In `app.py`, update these two lines before running locally:
   ```python
   app.config["SQLALCHEMY_DATABASE_URI"] = "your_database_url_here"
   app.config["JWT_SECRET_KEY"] = "your_secret_key_here"
   ```

   > ⚠️ For production, move these to environment variables and never hardcode them.

5. Run the app
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`

### Frontend Setup

1. Open the `bug-tracker-frontend/` folder
2. Open `index.html` in your browser
3. By default the frontend connects to the live API at `https://bug-tracker-api-kwyv.onrender.com`
4. To use your local backend, find and replace the base URL in each HTML file:
   ```
   https://bug-tracker-api-kwyv.onrender.com  →  http://localhost:5000
   ```

---

## 🔌 API Endpoints

### Auth (No token required)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and receive JWT token |

### Users (Token required)

| Method | Endpoint | Description | Who |
|---|---|---|---|
| GET | `/users` | Get all users | admin, manager |
| DELETE | `/users/<id>` | Delete a user | admin only |

### Projects (Token required)

| Method | Endpoint | Description | Who |
|---|---|---|---|
| GET | `/projects` | Get accessible projects | all roles |
| GET | `/projects/<id>` | Get a specific project | all roles |
| POST | `/projects` | Create a project | admin, manager |
| PUT | `/projects/<id>` | Update a project | admin, manager |
| DELETE | `/projects/<id>` | Delete a project | admin, manager (own) |

### Bugs (Token required)

| Method | Endpoint | Description | Who |
|---|---|---|---|
| GET | `/bugs` | Get all bugs | all roles |
| GET | `/bugs/<id>` | Get a specific bug | all roles |
| POST | `/bugs` | Create a bug | admin, tester |
| PUT | `/bugs/<id>` | Update a bug | admin, tester, developer |
| DELETE | `/bugs/<id>` | Delete a bug | admin only |

---

## 🔐 Authentication

1. Register a user via `/register`
2. Login via `/login` — receive a JWT token in the response
3. Include the token in all subsequent requests:
   ```
   Authorization: Bearer <your_token>
   ```

---

## 📝 Payload Examples

### Register
```json
{
    "name": "John",
    "email": "john@gmail.com",
    "password": "123456",
    "role": "manager"
}
```
Available roles: `admin` `manager` `tester` `developer`

### Login
```json
{
    "email": "john@gmail.com",
    "password": "123456"
}
```
Response includes: `Token`, `role`, `name`, `id`

### Create Project (admin / manager)
```json
{
    "name": "E-Commerce Website",
    "description": "Frontend and backend bug tracking",
    "manager_id": 2,
    "tester_id": 3,
    "developer_id": 4
}
```
> Note: `manager_id` is only required when an admin creates a project. Managers are automatically set as the manager of projects they create.

### Create Bug (admin / tester)
```json
{
    "title": "Login page crashes on submit",
    "description": "App throws 500 error when login form is submitted",
    "severity": "High",
    "priority": "High",
    "project_id": 1
}
```
> Bug is automatically assigned to the project's developer. Status defaults to `Open`.

### Update Bug — tester (title + status)
```json
{
    "title": "Updated title",
    "severity": "Medium",
    "status": "Re-Test"
}
```

### Update Bug — developer (status only)
```json
{
    "status": "In-Progress"
}
```

Available statuses: `Open` `Assigned` `In-Progress` `Fixed` `Re-Test` `Closed` `Re-Opened` `Rejected` `Hold`

---

## 🔄 Bug Status Flow

```
Open → Assigned → In-Progress → Fixed → Re-Test → Closed
                                             ↓
                                        Re-Opened → In-Progress
                                        Rejected
                                        Hold
```

---

## ⚠️ Known Limitations

- JWT tokens are not revoked on logout — tokens remain valid until expiry
- `JWT_SECRET_KEY` is currently hardcoded in `app.py` — move to environment variable before production use
- Database expires on Render free tier — will need renewal or migration to a paid plan for persistent data

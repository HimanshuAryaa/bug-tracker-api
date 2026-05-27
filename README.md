# Bug Tracker API
A REST API built for bug tracking for a organisation with JWT Authentication specific roles divided between users authorized user could do specific tasks.
- user with manager role could add/update projects, assign tester and developer to projects
- user with tester role could add/update bugs to the projects they are assigned
- user with developer role could update bugs to the projects they are assigned

## Features
- User registration and login
- JWT token authentication
- Get all Projects
- Get a specific Project with it's id
- Create a New Project
- Update a Project
- Delete a Project
- Protected routes — only authenticated users can create/update projects
- Get all Bugs
- Get a specific Bugs with it's id
- Create a new Bug
- Update a Bug
- Delete a Bug

## Tech Stack
- Python
- Flask
- SQLite
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Bcrypt

## Roles & Permissions table
| Role | admin | manager | tester | developer |
|------|-------|---------|--------|-----------|
| Permissions |  |  |  |  |
| Manage users | Yes | No | No | No |
| Create project | Yes | Yes | No | No |
| View all projects | Yes | Yes | Yes | Yes |
| Update project | Yes | Yes | No | No |
| Assign team | Yes | Yes | No | No |
| Report bug | Yes | No | Yes | No |
| Update bug status | Yes | No | Yes | Yes |
| View all bugs | Yes | Yes | Yes | Yes |
| Delete anything | Yes | No | No | No |

## Setup instructions
1. Clone the repository
2. Create virtual environment - 
    python -m venv venv
3. Activate virtual environment - 
    venv\Scripts\activate
4. Install dependencies - 
    pip install -r requirements.txt
5. Run the app - 
    python app.py

## API Endpoints

### Auth (No token required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and get JWT token |

### Projects (Token required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/projects` | Get all Projects |
| GET | `/projects/<int:id>` | Get Specific Project with id |
| POST | `/projects` | Create a Project |
| PUT | `/projects/<int:id>` | Update a Project |
| DELETE | `/projects/<int:id>` | Delete a Project |

### Bugs (Token required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/bugs` | Get all Bugs |
| GET | `/bugs/<int:id>` | Get Specific Bug with id |
| POST | `/bugs` | Create a Bug |
| PUT | `/bugs/<int:id>` | Update a Bug |
| DELETE | `/bugs/<int:id>` | Delete a bug |

## How to use authentication
1. Register a user via `/register`
2. Login via `/login` to get your token
3. Add the token to requests as Bearer Token in Authorization header

## Register Payload Example
```json
{
    "name": "John",
    "email": "john@gmail.com",
    "password": "123456",
    "role": "manager"
}
```
Available roles: `admin`, `manager`, `tester`, `developer`
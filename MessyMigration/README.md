User Management API – Refactored
A secure, modular, and production-ready user management API built with Flask. This project refactors a legacy monolithic codebase into a clean, modern architecture with well-separated concerns.

🔧 Key Features
👤 User CRUD: Create, retrieve, update, and delete users

🔐 Authentication: Login with secure password hashing

🔍 Search: Find users by name

🧠 In-Memory DB: Simple in-memory storage for demo purposes

🛡️ Security: Input & data validation, password rules

🧪 Testing: Unit tests with pytest

🧱 Clean Architecture: Separation of routes, services, models, and utilities

🌐 API Endpoints
Method	Endpoint	Description
GET	/users	Fetch all users
POST	/users	Create a new user
PUT	/user/<id>	Update an existing user
DELETE	/user/<id>	Delete a user
POST	/login	Authenticate user
GET	/search?name=xyz	Search users by name

📁 Project Structure
bash
Copy
Edit
messy-migration/
├── app.py                 # App factory and configuration
├── main.py                # Entry point for deployment
├── routes/                # HTTP endpoint logic
│   └── user_routes.py
├── services/              # Business logic
│   └── user_service.py
├── models/                # In-memory storage
│   └── db.py
├── utils/                 # Input validation
│   └── validation.py
├── tests/                 # Pytest test cases
│   └── test_users.py
├── init_db.py             # DB setup script
├── README.md              # You're reading this!
├── CHANGES.md             # Refactor documentation
├── .env.example           # Env var template
└── pyproject.toml         # Python dependencies
⚙️ Getting Started
✅ Prerequisites
Python 3.11+

pip

🛠️ Setup in 5 Steps
1. Clone the Project
bash
Copy
Edit
git clone <repo-url>
cd messy-migration
2. Install Dependencies
Option A: Manually

bash
Copy
Edit
pip install flask gunicorn pytest python-dotenv werkzeug email-validator
Option B: Using requirements.txt

bash
Copy
Edit
pip install -r requirements.txt
3. Configure Environment (Optional)
bash
Copy
Edit
cp .env.example .env
Edit .env:

env
Copy
Edit
SESSION_SECRET=your-secret-key
FLASK_ENV=development
FLASK_DEBUG=True
4. Initialize In-Memory Database
bash
Copy
Edit
python init_db.py
5. Start the Server
Development Mode

bash
Copy
Edit
python app.py
# or
flask run --host=0.0.0.0 --port=5000
Production Mode

bash
Copy
Edit
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
🧪 Verify It’s Working
Test with cURL:
bash
Copy
Edit
# API home
curl http://localhost:5000/

# Create user
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "email": "test@example.com", "password": "secure123"}'

# List users
curl http://localhost:5000/users
💡 Virtual Environment (Recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python init_db.py
python app.py
🧰 Troubleshooting
❌ ModuleNotFoundError: pip install flask

❌ Address already in use: Change port or kill the process

❌ 404 Not Found: Check URL for typos or extra spaces/line breaks

📘 API Examples
Create a User
bash
Copy
Edit
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","password":"secure123"}'
Login
bash
Copy
Edit
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"secure123"}'
Search Users
bash
Copy
Edit
curl http://localhost:5000/search?name=John
Update User
bash
Copy
Edit
curl -X PUT http://localhost:5000/user/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"John Updated"}'
Delete User
bash
Copy
Edit
curl -X DELETE http://localhost:5000/user/1
✅ API Response Format
Success:

json
Copy
Edit
{
  "id": 1,
  "name": "John",
  "email": "john@example.com"
}
Error:

json
Copy
Edit
{
  "error": "Invalid email format"
}
🔐 Validation Rules
Field	Rule
Name	2–100 chars, letters only
Email	Valid format, must be unique
Password	Min 6 chars, must include letters & numbers

📦 Testing
Run all tests:

bash
Copy
Edit
python -m pytest tests/
Run specific test:

bash
Copy
Edit
python -m pytest tests/test_users.py::TestUserAPI::test_create_user_valid

🧱 Database Schema
Column	Type	Constraints
id	INT	PRIMARY KEY, AUTO_INCREMENT
name	VARCHAR(100)	NOT NULL
email	VARCHAR(255)	UNIQUE, NOT NULL
password_hash	VARCHAR(255)	NOT NULL
created_at	TIMESTAMP	DEFAULT CURRENT_TIMESTAMP

🛡️ Security Features
Passwords hashed using Werkzeug

Input validation and sanitization

No sensitive info in error messages

🧩 Clean Architecture
Routes → Handle requests

Services → Business logic

Models → Data operations

Utils → Reusable helpers/validation


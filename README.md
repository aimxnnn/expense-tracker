# Expense Tracker

## 1. Project and Team

**Project Name:** Expense Tracker

Expense Tracker is a web application that allows users to register, log in and manage their personal expenses securely using authentication and JWT tokens.

### Team Members and Contributions

| Team Member | Endpoints Built | Description |
|---|---|---|
| Afifa | A1 – Register, A2 – Login | User registration and login with password hashing and JWT authentication |
| Shafff | A3 – Refresh, E1 – Get Expenses | Refresh access tokens and retrieve expenses belonging to the logged-in user |
| Aiman | E2 – Create Expense | Create and store expenses for the authenticated user |

## 2. Live App

**EC2 Public URL:** 

http://3.108.250.178:8001/docs

The application is deployed on an AWS EC2 instance.

## 3. How to Run It

### Prerequisites

Install the following on a fresh laptop:

- Python 3.12
- Node.js and npm
- Docker Desktop
- Git

### A. Run the Backend Locally

Open the terminal and navigate to the repository:


cd expense-tracker
cd backend

Create a virtual environment:

**Windows:**

python -m venv .venv
.venv\Scripts\activate


**Install dependencies:**

pip install -r requirements.txt


**Start the backend server:**

uvicorn main:app --reload --port 8001


Backend URL:

http://127.0.0.1:8001

API documentation:

http://127.0.0.1:8001/docs

### B. Run the Frontend Locally

Open a new terminal:
cd expense-tracker
cd frontend
npm install
npm run dev


The frontend runs at:

http://localhost:5173

### C. Run the Backend Using Docker

Navigate to the root repository:


cd expense-tracker


Build the Docker image:

docker build -t expense-tracker-backend ./backend


Run the Docker container:

docker run -d -p 8001:8001 -v "$(pwd)/data:/app/data" expense-tracker

Check running containers:


docker ps


Stop the container:
docker stop expense-tracker-container


Start the existing container again:

docker start expense-tracker-container


Remove the container:


docker rm expense-tracker-container

The backend will be accessible at:

http://localhost:8001

## 4. API Contract

### Endpoint Table

| ID | Method | Path | Request Body | Success Code |
|---|---|---|---|---|
| A1 | POST | `/register` | `{"username":"Afifa","email":"afifa@example.com","password":"password123"}` | 200 |
| A2 | POST | `/login` | `{"email":"afifa@example.com","password":"password123"}` | 200 |
| A3 | POST | `/refresh` | `{"refresh_token":"<refresh_token>"}` | 200 |
| E1 | GET | `/expenses` | No body. Requires Bearer access token. | 200 |
| E2 | POST | `/expenses` | `{"title":"Food","amount":250,"category":"Food","expense_date":"2026-11-23"}` | 201 |

### Authentication

The application uses JWT (JSON Web Tokens).

- Access tokens expire after 30 minutes.
- Refresh tokens expire after 7 days.
- Protected endpoints require an access token.
- Passwords are hashed using Argon2 before being stored.
- The authorization header format is:



### Error Rules

| Situation | HTTP Status Code | Error Message / Response |
|---|---|---|
| Email already registered | 409 | Email already exists |
| Invalid login credentials | 401 | Invalid email or password |
| Missing authorization header | 401 | Authentication required |
| Invalid authorization header | 401 | Invalid authorization header |
| Invalid or expired access token | 401 | Invalid or expired access token |
| Invalid or expired refresh token | 401 | Invalid or expired refresh token |
| User not found | 401 | User not found |
| Empty expense title or category | 422 | Title and category cannot be empty |
| Invalid email or missing required fields | 422 | Validation error |
| Amount less than or equal to zero | 422 | Validation error |
| Invalid date format | 422 | Validation error |

## 5. Database

The application uses SQLite with SQLAlchemy ORM.

The database file is stored at:


backend/data/expenses.db

There are two database tables.

### Table 1: users

| Column | Data Type | Description |
|---|---|---|
| id | Integer | Primary key |
| username | String | User's name |
| email | String | Unique email address |
| hashed_password | String | Argon2 hashed password |
| created_at | DateTime | Account creation timestamp |

### Table 2: expenses

| Column | Data Type | Description |
|---|---|---|
| id | Integer | Primary key |
| user_id | Integer | Foreign key referencing users.id |
| title | String | Expense title |
| amount | Float | Expense amount |
| category | String | Expense category |
| expense_date | Date | Date of expense |
| created_at | DateTime | Expense creation timestamp |

**Relationship:** One user can have multiple expenses. The `user_id` column in the expenses table connects each expense to its respective user.

## 6. Screenshots

### 1. User Registration

<img width="1600" height="1194" alt="WhatsApp Image 2026-11-23 at 2 01 00 PM" src="https://github.com/user-attachments/assets/5e892b72-723e-400f-9ee3-3e0163526392" />


Shows the registration page where a new user can create an account.

### 2. User Login

<img width="1600" height="1194" alt="WhatsApp Image 2026-11-23 at 2 01 00 PM (1)" src="https://github.com/user-attachments/assets/729b7c5e-ca3f-4bb5-b42c-c3a1a8ce53bd" />


Shows the login page where registered users can authenticate.

### 3. Dashboard

<img width="1600" height="958" alt="WhatsApp Image 2026-11-23 at 2 01 00 PM (2)" src="https://github.com/user-attachments/assets/39c71888-841d-4ded-8571-3acfbf66e489" />


Shows the expense dashboard after successful login.

### 4. Error Message

<img width="1600" height="1194" alt="WhatsApp Image 2026-11-23 at 2 01 01 PM" src="https://github.com/user-attachments/assets/f86ce11d-dcfa-4c82-9421-726a9109ef0f" />

<img width="1494" height="1420" alt="WhatsApp Image 2026-11-23 at 2 01 01 PM (1)" src="https://github.com/user-attachments/assets/9dcac3c4-57fe-43c6-b532-75d56cbbc8ba" />



Shows an error message when invalid information is entered.

### 5. API Endpoint Working in Swagger UI

<img width="1600" height="871" alt="WhatsApp Image 2026-11-23 at 2 02 55 PM" src="https://github.com/user-attachments/assets/e24f1c57-8563-4042-8fac-9aba016c59b7" />


Shows a successfully tested API endpoint in FastAPI Swagger documentation.

### 6. GitHub Actions

<img width="1600" height="871" alt="WhatsApp Image 2026-11-23 at 2 01 01 PM (2)" src="https://github.com/user-attachments/assets/4183043c-1ce3-4dde-93bd-4a53362f6361" />


Shows a successful GitHub Actions workflow run.

## 7. Known Issues

- The application currently uses SQLite, which may not be ideal for handling a large number of users.
- JWT secret key management needs improvement by moving the secret into environment variables.
- Refresh token revocation and logout functionality could be added.
- More automated backend and frontend tests could be implemented.
- Expense editing and deletion functionality could be added.
- Expense filtering, monthly summaries and graphical reports could be improved.

### Future Improvements

With more development time, we would like to:

- Implement edit and delete expense functionality.
- Add monthly and yearly expense reports.
- Add graphical expense analytics.
- Improve security through environment-based configuration.
- Add more automated testing.
- Improve the application's responsiveness and user experience.




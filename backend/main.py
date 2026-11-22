from datetime import date
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
import functions


app = FastAPI(
    title="Expense Tracker"
    )


# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# REQUEST MODEL

class RefreshToken(BaseModel):
    refresh_token: str

# REQUEST MODELS

class RegisterModel(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=1)


class LoginModel(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class ExpenseModel(BaseModel):
    title: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)
    expense_date: date

#Afifa
#REGISTER USER

@app.post("/register")
def register_user(data: RegisterModel):

    result = functions.register_user(
        data.username,
        data.email,
        data.password
    )

    if result is None:
        raise HTTPException(status_code=409, detail="Email already exists")

    return {
        "message": "User registered successfully"
    }

#Afifa
#LOGIN USER

@app.post("/login")
def login_user(data: LoginModel):

    result = functions.login_user(
        data.email,
        data.password
    )

    if result is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "access_token": result["access_token"],
        "refresh_token": result["refresh_token"],
        "token_type": "bearer"
    }


#Shafff
# A3 - GENERATE NEW ACCESS TOKEN

@app.post("/refresh")
def refresh_token(data: RefreshToken):

    new_access_token = functions.refresh_access_token(data.refresh_token)

    if new_access_token is None:
        raise HTTPException(status_code=401,detail="Invalid or expired refresh token")

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


# E1 - GET ALL EXPENSES OF LOGGED-IN USER

@app.get("/expenses")
def get_expenses(authorization: str = Header(None)):

    if authorization is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.replace("Bearer ", "", 1)

    email = functions.verify_token(token, "access")

    if email is None:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")

    expenses = functions.get_user_expenses(email)

    if expenses is None:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "expenses": expenses
    }


#Aiman
# E2 - CREATE EXPENSE FOR LOGGED-IN USER

@app.post("/expenses", status_code=201)
def create_expense(data: ExpenseModel, authorization: str = Header(None)):

    result = functions.create_expense(
        authorization,
        data.title,
        data.amount,
        data.category,
        data.expense_date
    )

    if result["error"] is not None:
        raise HTTPException(status_code=result["code"], detail=result["error"])

    return result["expense"]
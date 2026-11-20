from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import functions

from tables import Base, engine


app = FastAPI()

Base.metadata.create_all(bind=engine)


# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# REQUEST MODEL

class RefreshToken(BaseModel):
    refresh_token: str


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

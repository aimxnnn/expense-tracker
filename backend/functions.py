from sqlalchemy.orm import Session
from tables import engine, User, Expense
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
import jwt
from datetime import datetime, timedelta, timezone


# JWT SECRET KEY
SECRET_KEY = "Omggggg"
ALGORITHM = "HS256"

# Password hashing object
password_hasher = PasswordHasher()


#Shafff
# 1. CREATE TOKEN

def create_token(email, token_type):

    if token_type == "access":
        expiry = datetime.now(timezone.utc) + timedelta(minutes=30)
    else:
        expiry = datetime.now(timezone.utc) + timedelta(days=7)

    payload = {
        "sub": email,
        "type": token_type,
        "exp": expiry
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


# 2. VERIFY TOKEN

def verify_token(token, token_type):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email = payload.get("sub")
        actual_type = payload.get("type")

        if email is None or actual_type != token_type:
            return None

        return email

    except jwt.InvalidTokenError:
        return None



# A3 - GENERATE NEW ACCESS TOKEN

def refresh_access_token(refresh_token):

    email = verify_token(refresh_token, "refresh")

    if email is None:
        return None

    new_access_token = create_token(email, "access")

    return new_access_token


# E1 - GET ALL EXPENSES OF LOGGED-IN USER

def get_user_expenses(email):

    session = Session(engine)

    user = session.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        session.close()
        return None

    expenses = session.query(Expense).filter(
        Expense.user_id == user.id
    ).all()

    response = []

    for expense in expenses:

        temp_expense = {
            "id": expense.id,
            "user_id": expense.user_id,
            "title": expense.title,
            "amount": expense.amount,
            "category": expense.category,
            "expense_date": expense.expense_date,
            "created_at": expense.created_at
        }

        response.append(temp_expense)

    session.close()

    return response

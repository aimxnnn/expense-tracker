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


#Afifa
#REGISTER USER

def register_user(username, email, password):

    session = Session(engine)

    existing_user = session.query(User).filter(User.email == email).first()

    if existing_user:
        session.close()
        return None

    hashed_password = password_hasher.hash(password)

    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    session.add(new_user)
    session.commit()

    session.close()

    return True

#Afifa
#LOGIN USER

def login_user(email, password):

    session = Session(engine)

    user = session.query(User).filter(User.email == email).first()

    if user is None:
        session.close()
        return None

    try:
        password_hasher.verify(user.hashed_password,password)

    except VerifyMismatchError:
        session.close()
        return None

    access_token = create_token(user.email, "access")
    refresh_token = create_token(user.email, "refresh")

    session.close()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }



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


#Aiman
# E2 - CREATE EXPENSE FOR LOGGED-IN USER

def create_expense(token, title, amount, category, expense_date):

    if token is None:
        return {"error": "Authentication required", "code": 401, "expense": None}

    email = verify_token(token, "access")

    if email is None:
        return {"error": "Invalid or expired access token", "code": 401, "expense": None}

    if title.strip() == "" or category.strip() == "":
        return {"error": "Title and category cannot be empty", "code": 422, "expense": None}

    session = Session(engine)

    user = session.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        session.close()
        return {"error": "User not found", "code": 401, "expense": None}

    new_expense = Expense(
        user_id=user.id,
        title=title,
        amount=amount,
        category=category,
        expense_date=expense_date
    )

    session.add(new_expense)
    session.commit()
    session.refresh(new_expense)

    response = {
        "id": new_expense.id,
        "user_id": new_expense.user_id,
        "title": new_expense.title,
        "amount": new_expense.amount,
        "category": new_expense.category,
        "expense_date": new_expense.expense_date,
        "created_at": new_expense.created_at
    }

    session.close()

    return {"error": None, "code": 201, "expense": response}
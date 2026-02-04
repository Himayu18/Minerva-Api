from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .schemas import UserCreate, UserPublic, Token
from .security import hash_password, verify_password, create_access_token
from .database import get_db
from .crud import get_user_by_email, create_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserPublic)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, data.email):
        raise HTTPException(400, "User already exists")

    user = create_user(db, email=data.email, password_hash=hash_password(data.password))
    return {"id": user.id, "email": user.email}

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form.username
    user = get_user_by_email(db, email)

    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token(subject=email)
    return {"access_token": token}

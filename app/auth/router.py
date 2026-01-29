from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import UserCreate, UserPublic, Token
from .security import hash_password, verify_password, create_access_token
from .deps import get_user_store

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserPublic)
def register(data: UserCreate, users=Depends(get_user_store)):
    if data.email in users:
        raise HTTPException(400, "User already exists")

    user_id = len(users) + 1
    users[data.email] = {
        "id": user_id,
        "email": data.email,
        "password_hash": hash_password(data.password),
    }
    return {"id": user_id, "email": data.email}

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), users=Depends(get_user_store)):
    email = form.username
    user = users.get(email)

    if not user or not verify_password(form.password, user["password_hash"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token(subject=email)
    return {"access_token": token}


from fastapi import APIRouter, HTTPException, Depends, Header
from app.schemas.auth import RegisterRequest, LoginRequest, UserResponse, TokenResponse
from app.db.mongo import get_db
from app.services.auth_service import hash_password, verify_password, create_access_token, normalize_email
from jose import jwt, JWTError
from app.core.config import settings
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter(prefix="/api/auth", tags=["Auth"])

async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db = get_db()
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/register", response_model=UserResponse)
async def register(data: RegisterRequest):
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    db = get_db()
    email = normalize_email(data.email)
    existing = await db["users"].find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    doc = {
        "name": data.name.strip(),
        "email": email,
        "password_hash": hash_password(data.password),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    res = await db["users"].insert_one(doc)
    doc["_id"] = res.inserted_id
    return UserResponse(id=str(doc["_id"]), name=doc["name"], email=doc["email"], created_at=doc["created_at"])

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    db = get_db()
    email = normalize_email(data.email)
    user = await db["users"].find_one({"email": email})
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({"sub": str(user["_id"])})
    user_resp = UserResponse(id=str(user["_id"]), name=user["name"], email=user["email"], created_at=user["created_at"])
    return TokenResponse(access_token=token, user=user_resp)

@router.post("/logout")
async def logout(current_user=Depends(get_current_user)):
    # For JWT, logout is client-side token removal. Server can add blacklist if needed.
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def me(current_user=Depends(get_current_user)):
    return UserResponse(id=str(current_user["_id"]), name=current_user["name"], email=current_user["email"], created_at=current_user["created_at"])

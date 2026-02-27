from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..database import SessionLocal
from ..models import User
from ..auth import create_access_token, create_refresh_token

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(data: dict, db: Session = Depends(get_db)):
    hashed = pwd_context.hash(data["password"])
    user = User(name=data["name"], email=data["email"], password=hashed, role="admin")
    db.add(user)
    db.commit()
    return {"msg": "User created"}

@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data["email"]).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not pwd_context.verify(data["password"], user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access = create_access_token({"sub": str(user.id), "role": user.role})
    refresh = create_refresh_token({"sub": str(user.id)})

    return {"access_token": access, "refresh_token": refresh, "user": {"role": user.role}}

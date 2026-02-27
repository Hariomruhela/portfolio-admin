from fastapi import FastAPI
from .database import Base, engine
from .routes import auth, projects
from fastapi import Depends
from app.database import SessionLocal

from app.schemas import UserCreate


Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.get("/")
def home():
    return {"message": "API is running 🚀"}
app.include_router(auth.router, prefix="/auth")
app.include_router(projects.router, prefix="/projects")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/create-user")
def create_user(user: UserCreate):
    print(user)
    return user
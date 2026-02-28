from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, projects

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running 🚀"}

app.include_router(auth.router, prefix="/auth")
app.include_router(projects.router, prefix="/projects")
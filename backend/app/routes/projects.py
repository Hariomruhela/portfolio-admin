from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Project
import cloudinary.uploader

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
async def create_project(
    title: str,
    description: str,
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    upload = cloudinary.uploader.upload(await image.read())
    project = Project(
        title=title,
        description=description,
        image=upload["secure_url"]
    )
    db.add(project)
    db.commit()
    return project

@router.get("/")
def get_projects(page: int = 1, search: str = "", db: Session = Depends(get_db)):
    limit = 5
    offset = (page - 1) * limit

    query = db.query(Project).filter(Project.title.ilike(f"%{search}%"))
    total = query.count()
    projects = query.offset(offset).limit(limit).all()

    return {"projects": projects, "total": total}


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    total = db.query(Project).count()
    featured = db.query(Project).filter(Project.featured == True).count()
    return {"total_projects": total, "featured": featured}

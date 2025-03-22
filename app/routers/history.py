from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models import DetectionResult
from schemas import DetectionResult as DetectionResultSchema
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/history", response_model=List[DetectionResultSchema])
def get_history(page: int = 1, page_size: int = 10, search: str = "", db: Session = Depends(get_db)):
    query = db.query(DetectionResult)
    if search:
        query = query.filter(DetectionResult.image_path.ilike(f"%{search}%"))
    offset = (page - 1) * page_size
    results = query.order_by(DetectionResult.timestamp.desc()).offset(offset).limit(page_size).all()
    return results

import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
from detector import detect_persons
from database import SessionLocal
from models import DetectionResult

router = APIRouter()

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File không phải là ảnh")
    
    input_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(input_file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    output_filename = f"processed_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    output_file_path = os.path.join(OUTPUT_FOLDER, output_filename)
    
    try:
        num_people = detect_persons(input_file_path, output_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    detection = DetectionResult(num_people=num_people, image_path=output_file_path)
    db.add(detection)
    db.commit()
    db.refresh(detection)
    
    return {"num_people": num_people, "visualized_image": output_file_path}
    
@router.get("/download/{filename}")
async def download_image(filename: str):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File không tồn tại")
    return FileResponse(file_path)

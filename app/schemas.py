from pydantic import BaseModel
from datetime import datetime

class DetectionResultBase(BaseModel):
    num_people: int
    image_path: str

class DetectionResultCreate(DetectionResultBase):
    pass

class DetectionResult(DetectionResultBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

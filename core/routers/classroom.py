from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import Classroom, Course
from typing import List
from .. import schemas

router = APIRouter(prefix="/classrooms", tags=["Classrooms"])


# ---------------------------
# Retrieve all classrooms
# ---------------------------
@router.get("/", response_model=List[schemas.ClassroomResponse])
def get_classrooms(db: Session = Depends(get_db)):
    classrooms = db.query(Classroom).options(joinedload(Classroom.course)).all()
    return classrooms


# ---------------------------
# Add a classroom
# ---------------------------
@router.post("/", response_model=schemas.ClassroomResponse)
def add_classroom(request: schemas.ClassroomCreate, db: Session = Depends(get_db)):
    # Ensure course exists before creating classroom
    course = db.query(Course).filter(Course.id == request.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    new_classroom = Classroom(
        room_number=request.room_number,
        course_id=request.course_id,
        name=request.name
    )
    db.add(new_classroom)
    db.commit()
    db.refresh(new_classroom)
    return new_classroom


# ---------------------------
# Get a single classroom
# ---------------------------
@router.get("/{id}", response_model=schemas.ClassroomResponse)
def get_classroom(id: int, db: Session = Depends(get_db)):
    classroom = db.query(Classroom).options(joinedload(Classroom.course)).filter(Classroom.id == id).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return classroom

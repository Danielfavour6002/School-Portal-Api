from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import Base, engine, get_db
from ..models import Student, Teacher, Course, Classroom, Assignment, student_course
from typing import List
from .. import schemas

router = APIRouter(prefix="/classroom", tags=["classroom"])

#classroom
#retrieve all classrooms
@router.get("/", response_model= List[schemas.ClassroomResponse])
def get_classrooms(db: Session = Depends(get_db)):
    classrooms = db.query(Classroom).all()
    return classrooms

#add a classroom
@router.post("/", response_model= schemas.ClassroomResponse)
def add_student(request:schemas.ClassroomCreate, db:Session = Depends(get_db)):
    new_classroom = Classroom(room_number=request.room_number, course_id= request.course_id, name = request.name)
    db.add(new_classroom)
    db.commit()
    db.refresh(new_classroom)
    return new_classroom

#get a single classrooom
@router.get("/{id}", response_model= schemas.ClassroomResponse)
def get_students(id : int , db: Session = Depends(get_db)):
    classroom = db.query(Classroom).filter(Classroom.id == id).first()
    return classroom
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import Base, engine, get_db, create_table
from ..models import Student, Teacher, Course, Classroom, Assignment, student_course
from typing import List
from .. import schemas
from ..utilities import PasswordHasher

router = APIRouter(prefix="/teachers", tags=["teachers"])
PH = PasswordHasher()
#retrieve all teachers
@router.get("/", response_model= List[schemas.TeacherBase])
def get_teachers(db: Session = Depends(get_db)):
    teacher = db.query(Teacher).all()
    return teacher
#add a teacher
@router.post("/", response_model= schemas.TeacherBase)
def add_teacher(request:schemas.Teacher, db:Session = Depends(get_db)):
    new_teacher = Teacher(name=request.name, email= request.email, password=PH.hash_password(request.password))
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher

#get a single teacher
@router.get("/{id}", response_model= schemas.TeacherBase)
def get_teacher(id : int , db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == id).first()
    return teacher
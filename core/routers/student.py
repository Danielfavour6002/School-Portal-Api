from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session, joinedload
from ..database import Base, engine, get_db, create_table
from ..models import Student, Teacher, Course, Classroom, Assignment, student_course
from typing import List, Annotated
from .. import schemas
from ..utilities import PasswordHasher
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/students", tags=["Students"])

#students
PH = PasswordHasher()
#retrieve all students
@router.get("/", response_model= List[schemas.StudentBase])
def get_students(db: Session = Depends(get_db)):
    student = db.query(Student).all()
    return student
#sign-up a student
@router.post("/signup", response_model= schemas.StudentBase)
def add_student(request:schemas.Student, db:Session = Depends(get_db)):
    new_student = Student(name=request.name, email=request.email, password=PH.hash_password(password=request.password))
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.post("/login", response_model= schemas.StudentBase)
def add_student(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email==form_data.username).first()
    if not student:
        raise HTTPException(status_code=404, detail="Incorrect details: Email not found")
    password_check = PH.verify_password(form_data.password,student.password)
    if not password_check:
        raise HTTPException(status_code=400, detail="Incorrect details: Incorrect password")
    db.commit()
    db.refresh(student)
    return {"access_token": student.email, "token_type": "bearer"}
    

#get a single student
@router.get("/{id}", response_model= schemas.StudentBase)
def get_students(id : int , db: Session = Depends(get_db)):
    student = db.query(Student).options(joinedload(Student.courses)).filter(Student.id == id).first()
    return student

#list of courses enrolled by a student
@router.get("/students/{id}/courses", response_model=schemas.StudentWithCourses)
def enrolled_student(id :int,  db: Session = Depends(get_db)):
        student = db.query(Student).filter(Student.id==id).first()
        if not student:
            raise HTTPException(status_code=404, detail="student not found")
        courses = student.courses
        return courses
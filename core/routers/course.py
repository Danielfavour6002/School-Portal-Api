from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import Base, engine, get_db
from ..models import Student, Teacher, Course, Classroom, Assignment, student_course
from typing import List
from .. import schemas


router = APIRouter(prefix="/courses", tags=["course"])

#courses
#retrieve all courses
@router.get("/", response_model= List[schemas.Course])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses
#add a course
@router.post("/", response_model= schemas.Course)
def add_course(request:schemas.CourseCreate, db:Session = Depends(get_db)):
    new_course = Course(title=request.title, description= request.description, teacher_id=request.teacher_id)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

#get a single course
@router.get("/courses/{id}", response_model= schemas.Course)
def get_course(id : int , db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == id).first()
    return course

#enrollment
@router.post("/{course_id}/enroll/{student_id}", response_model=schemas.EnrollResponse)
def enroll( course_id:int, student_id=int,  db:Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id==student_id).first()
    course = db.query(Course).filter(Course.id==course_id).first()
    if not student or not course:
        raise HTTPException(status_code=404, detail="student or course not found")
    if course in student.courses:
        raise HTTPException(status_code=400, detail="student already enrolled")
    student.courses.append(course)
    db.commit()
    db.refresh(student)
    return schemas.EnrollResponse(
    message=f"Student {student.id} enrolled in course {course.id}",
    student=student,
    course=course)

#get list of student enrolled in acourse
@router.get("{id}/students", response_model=schemas.CourseWithStudent)
def enrolled_student(id :int,  db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id==id).first()
    if not course:
        raise HTTPException(status_code=404, detail="course not found")
    return course


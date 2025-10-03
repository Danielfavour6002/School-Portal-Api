from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import Course, StudentProfile
from typing import List
from .. import schemas

router = APIRouter(prefix="/courses", tags=["Courses"])


# ---------------------------
# Get all courses
# ---------------------------
@router.get("/", response_model=List[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses


# ---------------------------
# Add a course
# ---------------------------
@router.post("/", response_model=schemas.CourseResponse)
def add_course(request: schemas.CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(
        title=request.title,
        description=request.description,
        teacher_id=request.teacher_id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


# ---------------------------
# Get a single course
# ---------------------------
@router.get("/{id}", response_model=schemas.CourseResponse)
def get_course(id: int, db: Session = Depends(get_db)):
    course = db.query(Course).options(joinedload(Course.students)).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


# ---------------------------
# Enroll a student in a course
# ---------------------------
@router.post("/{course_id}/enroll/{student_id}", response_model=schemas.EnrollResponse)
def enroll(course_id: int, student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()

    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or Course not found")

    if course in student.courses:
        raise HTTPException(status_code=400, detail="Student already enrolled")

    student.courses.append(course)
    db.commit()
    db.refresh(student)

    return schemas.EnrollResponse(
        message=f"Student {student.id} enrolled in course {course.id}",
        student=student,
        course=course
    )


# ---------------------------
# Get list of students enrolled in a course
# ---------------------------
@router.get("/{id}/students", response_model=schemas.CourseStudentsResponse)
def enrolled_students(id: int, db: Session = Depends(get_db)):
    course = db.query(Course).options(joinedload(Course.students)).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return {
        "course_id": course.id,
        "course_title": course.title,
        "students": course.students
    }

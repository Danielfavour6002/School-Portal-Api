from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import User, StudentProfile, Course
from typing import List, Annotated
from .. import schemas
from ..utilities import PasswordHasher
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/students", tags=["Students"])
PH = PasswordHasher()


# ---------------------------
# Get all students
# ---------------------------
@router.get("/", response_model=List[schemas.StudentProfileResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(StudentProfile).options(joinedload(StudentProfile.user)).all()
    return students


# ---------------------------
# Signup a student
# ---------------------------
@router.post("/signup", response_model=schemas.StudentProfileResponse)
def signup_student(request: schemas.UserCreate, db: Session = Depends(get_db)):
    if request.role != schemas.RoleEnum.student:
        raise HTTPException(status_code=400, detail="Role must be 'student'")

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create User
    new_user = User(
        name=request.name,
        email=request.email,
        password=PH.hash_password(request.password),
        role=request.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create StudentProfile
    new_student_profile = StudentProfile(user_id=new_user.id)
    db.add(new_student_profile)
    db.commit()
    db.refresh(new_student_profile)

    return new_student_profile


# ---------------------------
# Login a student
# ---------------------------
@router.post("/login", response_model=schemas.Token)
def login_student(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username, User.role == schemas.RoleEnum.student).first()
    if not user:
        raise HTTPException(status_code=404, detail="Student not found")

    if not PH.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    # TODO: replace with real JWT generation
    return {"access_token": user.email, "token_type": "bearer"}


# ---------------------------
# Get a single student
# ---------------------------
@router.get("/{id}", response_model=schemas.StudentProfileResponse)
def get_student(id: int, db: Session = Depends(get_db)):
    student = db.query(StudentProfile).options(
        joinedload(StudentProfile.user),
        joinedload(StudentProfile.courses)
    ).filter(StudentProfile.id == id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# ---------------------------
# List of courses enrolled by a student
# ---------------------------
@router.get("/{id}/courses", response_model=List[schemas.CourseBase])
def enrolled_courses(id: int, db: Session = Depends(get_db)):
    student = db.query(StudentProfile).options(joinedload(StudentProfile.courses)).filter(StudentProfile.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student.courses

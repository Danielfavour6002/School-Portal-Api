from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, TeacherProfile
from .. import schemas
from ..utilities import PasswordHasher
from typing import List

router = APIRouter(prefix="/teachers", tags=["teachers"])
PH = PasswordHasher()


# ---------------------------
# Get all teachers
# ---------------------------
@router.get("/", response_model=List[schemas.TeacherProfileResponse])
def get_teachers(db: Session = Depends(get_db)):
    teachers = db.query(TeacherProfile).all()
    return teachers


# ---------------------------
# Add a new teacher
# ---------------------------
@router.post("/", response_model=schemas.TeacherProfileResponse)
def add_teacher(request: schemas.UserCreate, db: Session = Depends(get_db)):
    # ✅ ensure only teachers can be created here
    if request.role != schemas.RoleEnum.teacher:
        raise HTTPException(status_code=400, detail="Role must be 'teacher'")

    # check if email already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # create User
    new_user = User(
        name=request.name,
        email=request.email,
        password=PH.hash_password(request.password),
        role=request.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # create TeacherProfile
    new_teacher_profile = TeacherProfile(user_id=new_user.id)
    db.add(new_teacher_profile)
    db.commit()
    db.refresh(new_teacher_profile)

    return new_teacher_profile


# ---------------------------
# Get single teacher
# ---------------------------
@router.get("/{id}", response_model=schemas.TeacherProfileResponse)
def get_teacher(id: int, db: Session = Depends(get_db)):
    teacher = db.query(TeacherProfile).filter(TeacherProfile.id == id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

from fastapi import FastAPI, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from .database import get_db
from .routers import classroom, course, teacher, student
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from . import schemas, models
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime


app = FastAPI(
    title="School Management System",
    servers=[
        {"url" : "http://127.0.0.1:8001", "description": "Local server"},
        {"url" : "https://school-portal-api-ll9w.onrender.com/", "description": "prod server"},
        
    ])

# create_table()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://v0.app", ],  # Add this domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(course.router)
app.include_router(classroom.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@app.get("/dashboard", response_model=schemas.Dashboard)
def dashboard(db: Session = Depends(get_db)):
    # Assuming your User model has a 'role' field (e.g., "student", "teacher")
    students = db.query(models.User).filter(models.User.role == "student").count()
    teachers = db.query(models.User).filter(models.User.role == "teacher").count()
    
    # Other tables remain the same
    courses = db.query(models.Course).count()
    classrooms = db.query(models.Classroom).count()
    
    return schemas.Dashboard(
        students=students,
        teachers=teachers,
        courses=courses,
        classrooms=classrooms
    )


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
#allocation
#assignment

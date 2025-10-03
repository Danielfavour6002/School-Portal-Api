from pydantic import BaseModel, EmailStr
from typing import List, Optional
from enum import Enum


# ---------------------------
# ROLES
# ---------------------------
class RoleEnum(str, Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"


# ---------------------------
# USER (Authentication layer)
# ---------------------------
class UserBase(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# ---------------------------
# STUDENT PROFILE
# ---------------------------
class StudentProfileBase(BaseModel):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class StudentProfileResponse(StudentProfileBase):
    user: UserBase
    courses: Optional[List["CourseBase"]] = []


# ---------------------------
# TEACHER PROFILE
# ---------------------------
class TeacherProfileBase(BaseModel):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class TeacherProfileResponse(TeacherProfileBase):
    user: UserBase
    courses_taught: Optional[List["CourseBase"]] = []


# ---------------------------
# COURSES
# ---------------------------
class CourseBase(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True


class CourseCreate(BaseModel):
    title: str
    description: str
    teacher_id: int


class CourseResponse(CourseBase):
    teacher: Optional["TeacherProfileResponse"]
    students: Optional[List["StudentProfileResponse"]] = []
    classroom: Optional["ClassroomResponse"]
    assignments: Optional[List["AssignmentResponse"]] = []


class CourseStudentsResponse(BaseModel):
    course_id: int
    course_title: str
    students: List[StudentProfileResponse]

    class Config:
        from_attributes = True


# ---------------------------
# ASSIGNMENTS
# ---------------------------
class AssignmentBase(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        from_attributes = True


class AssignmentCreate(BaseModel):
    course_id: int
    student_id: int
    question: str
    answer: str


class AssignmentResponse(AssignmentBase):
    course: Optional["CourseBase"]
    student: Optional["StudentProfileResponse"]


# ---------------------------
# CLASSROOM
# ---------------------------
class ClassroomCreate(BaseModel):
    room_number: int
    course_id: int
    name: str


class ClassroomResponse(BaseModel):
    id: int
    room_number: int
    course_id: int
    name: str

    class Config:
        from_attributes = True


# ---------------------------
# ENROLLMENT
# ---------------------------
class EnrollResponse(BaseModel):
    message: str
    student: StudentProfileResponse
    course: CourseBase

    class Config:
        from_attributes = True


# ---------------------------
# DASHBOARD
# ---------------------------
class Dashboard(BaseModel):
    students: int
    teachers: int
    courses: int
    classrooms: int


# ---------------------------
# Rebuild Forward References
# ---------------------------
StudentProfileResponse.model_rebuild()
TeacherProfileResponse.model_rebuild()
CourseResponse.model_rebuild()
AssignmentResponse.model_rebuild()
ClassroomResponse.model_rebuild()

from pydantic import BaseModel
from typing import List, Optional

# ---------------------------
# STUDENTS
# ---------------------------
class StudentBase(BaseModel):
    id: int                           # ✅ unique identifier
    name: str
    email: str

    class Config:
        from_attributes = True        # ✅ allows ORM objects → schema


class StudentCreate(BaseModel):
    name: str
    email: str
    password: str                     # ✅ password only used at creation


class StudentResponse(StudentBase):
    courses: Optional[List["CourseBase"]] = []  # forward ref → needs rebuild


class StudentLogin(BaseModel):
    email: str
    password: str


class StudentToken(BaseModel):
    access_token: str
    token_type: str


# ---------------------------
# TEACHERS
# ---------------------------
class TeacherBase(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class TeacherCreate(BaseModel):
    name: str
    email: str
    password: str


class TeacherResponse(TeacherBase):
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
    teacher: Optional["TeacherBase"]
    students: Optional[List["StudentBase"]] = []
    classroom: Optional["ClassroomResponse"]
    assignments: Optional[List["AssignmentResponse"]] = []

class CourseStudentsResponse(BaseModel):
    course_id: int
    course_title: str
    students: List[StudentBase]

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
    student: Optional["StudentBase"]


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
    student: StudentBase
    course: CourseBase

    class Config:
        from_attributes = True


# ---------------------------
# Rebuild Forward References
# ---------------------------
StudentResponse.model_rebuild()
TeacherResponse.model_rebuild()
CourseResponse.model_rebuild()
AssignmentResponse.model_rebuild()
ClassroomResponse.model_rebuild()

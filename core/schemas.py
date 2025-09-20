from pydantic import BaseModel
from typing import List, Optional

#STUDENTS
class StudentB(BaseModel):
    name: str
    email : str
     

class StudentBase(StudentB):
    name: str
    email : str
    courses : Optional[List["Course"]] = []
    class config():
        from_attributes = True
class StudentWithCourses(StudentB):
    courses : Optional[List["CourseBase"]] = []
   
class Student(StudentB):
    password: str

class StudentLogin(BaseModel):
    email : str
    password : str
class StudentToken(BaseModel):
    access_token : str
    token_type  :str
    
#TEACHERS
class TeacherBase(BaseModel):
    name: str
    email : str

class Teacher(TeacherBase):
    password : str

class TeacherResponse(TeacherBase):
    courses_taught : Optional[List["CourseBase"]] = []

#COURSE
class CourseBase(BaseModel):
    title : str
    description : str

class CourseCreate(CourseBase):
    password : str
    teacher_id : int

class Course(CourseBase):
    teacher : Optional["TeacherBase"]
    students : Optional[List["StudentB"]] = []
    #probable error
    classroom : Optional["ClassroomResponse"]
    assignment : Optional[List["AssignmentBase"]] = []
    class config():
        from_attributes = True

class CourseWithStudent(CourseBase):
    students : Optional[List["StudentB"]] = []

#ASSIGNMENT
class AssignmentBase(BaseModel):
    course_id : Optional[CourseBase]
    student_id : Optional[StudentB]
    question : str
    answer : str

class AssignmentResponse(AssignmentBase):
    class config():
        from_attributes = True

#CLASSROOM
class ClassroomCreate(BaseModel):
    room_number:int
    course_id: int
    name : str
    
    
class ClassroomResponse(ClassroomCreate):
    
    class config():
        from_attributes = True

# class EnrollBase(BaseModel):
#     student_id : int
    

class EnrollResponse(BaseModel):
    message: str
    student: StudentB
    course: CourseBase

    class Config:
        from_attributes = True



# 🔑 Call rebuild at the end
StudentBase.model_rebuild()
TeacherResponse.model_rebuild()
Course.model_rebuild()
ClassroomResponse.model_rebuild()

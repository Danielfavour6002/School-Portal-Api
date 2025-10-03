from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import Student, Teacher, Course, Classroom, Assignment, student_course
from typing import List
from . import schemas



app = FastAPI()
app.include_router()

#students

#retrieve all students
@app.get("/students", response_model= List[schemas.StudentBase])
def get_students(db: Session = Depends(get_db)):
    student = db.query(Student).all()
    return student
#add a student
@app.post("/add_student", response_model= schemas.StudentBase)
def add_student(request:schemas.Student, db:Session = Depends(get_db)):
    new_student = Student(name=request.name, email= request.email, password=request.password)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

#get a single student
@app.get("/students/{id}", response_model= schemas.StudentBase)
def get_students(id : int , db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    return student


#courses
#retrieve all courses
@app.get("/courses", response_model= List[schemas.Course])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses
#add a course
@app.post("/add_course", response_model= schemas.Course)
def add_course(request:schemas.CourseCreate, db:Session = Depends(get_db)):
    new_course = Course(title=request.title, description= request.description, teacher_id=request.teacher_id)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

#get a single course
@app.get("/courses/{id}", response_model= schemas.Course)
def get_course(id : int , db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == id).first()
    return course

#retrieve all teachers
@app.get("/teachers", response_model= List[schemas.TeacherBase])
def get_teachers(db: Session = Depends(get_db)):
    teacher = db.query(Teacher).all()
    return teacher
#add a teacher
@app.post("/add_teacher", response_model= schemas.TeacherBase)
def add_teacher(request:schemas.Teacher, db:Session = Depends(get_db)):
    new_teacher = Teacher(name=request.name, email= request.email, password=request.password)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher

#get a single teacher
@app.get("/teachers/{id}", response_model= schemas.TeacherBase)
def get_teacher(id : int , db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == id).first()
    return teacher

#classroom
#retrieve all classrooms
@app.get("/classrooms", response_model= List[schemas.ClassroomBase])
def get_classrooms(db: Session = Depends(get_db)):
    classrooms = db.query(Classroom).all()
    return classrooms


#add a classroom
@app.post("/add_classroom", response_model= schemas.ClassroomBase)
def add_student(request:schemas.Classroom, db:Session = Depends(get_db)):
    new_classroom = Classroom(room_number=request.room_number, course_id= request.course_id)
    db.add(new_classroom)
    db.commit()
    db.refresh(new_classroom)
    return new_classroom

#get a single classrooom
@app.get("/classrooms/{id}", response_model= schemas.ClassroomBase)
def get_students(id : int , db: Session = Depends(get_db)):
    classroom = db.query(Classroom).filter(Classroom.id == id).first()
    return classroom

#enrollment
@app.post("/course_id/enroll", response_model=schemas.EnrollResponse)
def enroll(request:schemas.EnrollBase, db:Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id==request.Student_id).first()
    course = db.query(Course).filter(Course.id==request.course_id).first()
    if not student or not course:
        raise HTTPException(status_code=404, detail="student or course not found")
    if course in student.courses:
        raise HTTPException(status_code=400, detail="student already enrolled")
    student.courses.append(course)
    db.commit()
    return f"message: student {student.id} enrolled in course {course.id}"

#get list of student enrolled in acourse
@app.get("/courses/{id}/students", response_model=schemas.Course)
def enrolled_student(id :int,  db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id==id).first()
    if not course:
        raise HTTPException(status_code=404, detail="course not found")
    students = course.students
    return students
#list of course enrolled by a student
@app.get("/students/{id}/courses", response_model=schemas.StudentBase)
def enrolled_student(id :int,  db: Session = Depends(get_db)):
    try: 
        student = db.query(Student).filter(Student.id==id).first()
        if not student:
            raise HTTPException(status_code=404, detail="student not found")
        courses = student.courses
        return courses
    except Exception as e: 
        return {"status": "error", "messsage": e}
 



#allocation
#assignment

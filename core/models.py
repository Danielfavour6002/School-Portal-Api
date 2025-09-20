from sqlalchemy import String, Integer, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

# Association table for many-to-many
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("student.id")),
    Column("course_id", Integer, ForeignKey("course.id"))
)

class Student(Base):
    __tablename__ = "student"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    
    # Many-to-many with Course
    courses = relationship("Course", secondary=student_course, back_populates="students")


class Teacher(Base):
    __tablename__ = "teacher"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    
    # One-to-many with Course
    courses_taught: Mapped[list["Course"]] = relationship("Course", back_populates="teacher")


class Course(Base):
    __tablename__ = "course"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    
    # Many-to-many with Student
    students = relationship("Student", secondary=student_course, back_populates="courses")
    #one to one with classroom
    classroom: Mapped["Classroom"] = relationship("Classroom", uselist=False, back_populates="course_class")
    # Many-to-one with Teacher
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="courses_taught")
    #one to many with assignment
    assignment : Mapped[list["Assignment"]] = relationship("Assignment", back_populates="course_ass")


class Classroom(Base):
    __tablename__ = "classroom"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    room_number: Mapped[int] = mapped_column(Integer)
    name : Mapped[str] = mapped_column(String)
    
    # Example: One-to-one with Course
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"), unique=True)
    course_class: Mapped["Course"] = relationship("Course")

class Assignment(Base):
    __tablename__ = "assignnments"
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    course_id : Mapped[int] = mapped_column(ForeignKey("course.id"), unique=True)
    course_ass : Mapped["Course"] = relationship("Course", back_populates="assignment")
    student_id : Mapped[int] = mapped_column(ForeignKey("student.id"))
    question : Mapped[str] = mapped_column(String)
    answer : Mapped[str] = mapped_column(String)
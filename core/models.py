from sqlalchemy import String, Integer, Table, Column, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
from enum import Enum

# -------------------------
# ENUM for roles
# -------------------------
class RoleEnum(str, Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

# -------------------------
# User Table (AUTH BASE)
# -------------------------
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    role: Mapped[RoleEnum] = mapped_column(SqlEnum(RoleEnum), nullable=False)

    # Relationships
    student_profile: Mapped["StudentProfile"] = relationship("StudentProfile", back_populates="user", uselist=False)
    teacher_profile: Mapped["TeacherProfile"] = relationship("TeacherProfile", back_populates="user", uselist=False)


# -------------------------
# Student Profile
# -------------------------
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("student_profiles.id")),
    Column("course_id", Integer, ForeignKey("course.id"))
)

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship("User", back_populates="student_profile")
    courses: Mapped[list["Course"]] = relationship("Course", secondary=student_course, back_populates="students")


# -------------------------
# Teacher Profile
# -------------------------
class TeacherProfile(Base):
    __tablename__ = "teacher_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship("User", back_populates="teacher_profile")
    courses_taught: Mapped[list["Course"]] = relationship("Course", back_populates="teacher")


# -------------------------
# Course
# -------------------------
class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))

    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher_profiles.id"))

    # Relationships
    teacher: Mapped["TeacherProfile"] = relationship("TeacherProfile", back_populates="courses_taught")
    students: Mapped[list["StudentProfile"]] = relationship("StudentProfile", secondary=student_course, back_populates="courses")
    classroom: Mapped["Classroom"] = relationship("Classroom", uselist=False, back_populates="course_class")
    assignment: Mapped[list["Assignment"]] = relationship("Assignment", back_populates="course_ass")


# -------------------------
# Classroom
# -------------------------
class Classroom(Base):
    __tablename__ = "classroom"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    room_number: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)

    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"), unique=True)
    course_class: Mapped["Course"] = relationship("Course", back_populates="classroom")


# -------------------------
# Assignment
# -------------------------
class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("student_profiles.id"))

    question: Mapped[str] = mapped_column(String)
    answer: Mapped[str] = mapped_column(String)

    course_ass: Mapped["Course"] = relationship("Course", back_populates="assignment")

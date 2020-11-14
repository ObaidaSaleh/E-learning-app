import click

import requests
import json

from flask import current_app, g, url_for
from flask.cli import with_appcontext

from uimpactify.cli.db import ADMIN_USER
from uimpactify.cli import auth_util
from uimpactify.cli import course_util
from uimpactify.cli import user_util
from uimpactify.cli import feedback_util

from uimpactify.controller import routes


@click.command("auth-test")
@with_appcontext
def auth_test():
    auth_run_test()

def auth_run_test():
    # Create a new user, sign in as the user, and delete the user
    user = {"email": "test_user@uimpactify.com", "password": "password"}
    user_id = auth_util.signup(user)
    user_token = auth_util.login(user)
    user_util.delete_self(user_token)


@click.command("course-test")
@with_appcontext
def course_test():
    course_run_test()

def course_run_test():
    # CREATING SAMPLE DATA
    access_token = auth_util.login()

    # creating a separate instructor user
    inst_json = {
        "name": "instructor person",
        "email": "instructor_person@uimpactify.com",
        "password": "password",
        "roles": {"student": True, "instructor": True},
        }
    inst_id = auth_util.signup(inst_json)
    inst_token = auth_util.login(inst_json)

    # creating a test student
    s_json = {
        "name": "student",
        "email": "student_person@uimpactify.com",
        "password": "password",
        }
    s_id = auth_util.signup(s_json)
    s_token = auth_util.login(s_json)

    # creating a bunch of courses
    c1_json = { "name": "testCourseOne", }
    c2_json = { "name": "testCourseTwo", }
    c3_json = { "name": "testCourseThree", }

    c1 = course_util.create_course(access_token, c1_json)
    c2 = course_util.create_course(access_token, c2_json)
    c3 = course_util.create_course(inst_token, c3_json)

    # enroll a student in some courses
    course_util.enroll_student(s_token, c2)
    course_util.enroll_student(s_token, c3)

    # getting info on the created courses
    course_util.get_all_courses(access_token)
    course_util.get_courses_by_instructor(inst_token)
    course_util.get_courses_with_student(s_token)

    # create feedback for some courses
    f1_json = {
        "comment": "Hello readers of this public feedback",
        "course": c2,
        "public": True
    }
    f1 = feedback_util.create_feedback(s_token, f1_json)

    f2_json = {
        "comment": "Hello instructor! Moo!",
        "course": c3,
        "public": False
    }
    f2 = feedback_util.create_feedback(s_token, f2_json)

    # getting the public feedback
    feedback_util.get_feedback(s_token, c2)
    # getting private feedback (empty)
    feedback_util.get_feedback(s_token, c3)
    # getting private feedback as instructor (not empty)
    feedback_util.get_feedback(inst_token, c3)

    # CLEAN UP
    # disenroll a student
    course_util.disenroll_student(s_token, c2)

    # removing the new users
    user_util.delete_self(inst_token)
    user_util.delete_self(s_token)

    # removing new courses
    course_util.delete_course(access_token, c1)
    course_util.delete_course(access_token, c2)

    # getting all courses again to show that they are gone
    course_util.get_all_courses(access_token)

@click.command("test")
@with_appcontext
def test_all():
    print(
        "----------------------------\n" +
        "RUNNING AUTHENTICATION TESTS\n" +
        "----------------------------\n"
        )
    auth_run_test()

    print(
        "----------------------------\n" +
        "RUNNING COURSE RELATED TESTS\n" +
        "----------------------------\n"
        )
    course_run_test()


@click.command("init-data")
@with_appcontext
def init_data():
    # SETUP USERS
    # Create instructors
    inst1_json = {
        "name": "Instructor 1",
        "email": "inst1@uimpactify.com",
        "password": "password",
        "roles": {"student": True, "instructor": True},
        }
    inst1 = auth_util.signup(inst1_json)
    inst1_token = auth_util.login(inst1_json)
    
    inst2_json = {
        "name": "Instructor 2",
        "email": "inst2@uimpactify.com",
        "password": "password",
        "roles": {"instructor": True},
        }
    inst2 = auth_util.signup(inst2_json)
    inst2_token = auth_util.login(inst2_json) 
    
    # Create students
    s1_json = {
        "name": "Student 1", 
        "email": "s1@uimpactify.com", 
        "password": "password",
        }
    s1 = auth_util.signup(s1_json)
    s1_token = auth_util.login(s1_json)
    
    s2_json = {
        "name": "Student 2", 
        "email": "s2@uimpactify.com", 
        "password": "password",
        }
    s2 = auth_util.signup(s2_json)
    s2_token = auth_util.login(s2_json)
    
    s3_json = {
        "name": "Student 3", 
        "email": "s3@uimpactify.com", 
        "password": "password",
        }
    s3 = auth_util.signup(s3_json)
    s3_token = auth_util.login(s3_json)
    
    # Create NPOs
    npo1_json = {
        "name": "Organization 1", 
        "email": "npo1@uimpactify.com", 
        "password": "password",
        "roles": {"organization": True},
        }
    npo1 = auth_util.signup(npo1_json)
    npo1_token = auth_util.login(npo1_json)


    # SETUP COURSES
    # Create courses taught by different instructors (with some being published)
    c1_json = { "name": "Course One (I1)", }
    c2_json = { "name": "Course Two (I1)", "published": True}
    c3_json = { "name": "Course Three (I2)", "published": True}

    c1 = course_util.create_course(inst1_token, c1_json)
    c2 = course_util.create_course(inst1_token, c2_json)
    c3 = course_util.create_course(inst2_token, c3_json)

    # Enroll students in courses
    course_util.enroll_student(s1_token, c1)
    course_util.enroll_student(s1_token, c2)
    course_util.enroll_student(s2_token, c2)
    course_util.enroll_student(s3_token, c2)

    # Add feedback to courses
    f1_json = {
        "comment": "This course was the best course I've ever taken and I'm so glad it was able to provide so much value it's just absolutely insane I loved it and I feel like a better human being for taking it and I'm about to change the world by removing financial burgers one step at a time. Nom nom nom.",
        "course": c2,
        "public": True
    }
    f1 = feedback_util.create_feedback(s1_token, f1_json)

    f2_json = {
        "comment": "Sick course. Keep it up homie.",
        "course": c2,
        "public": False
    }
    f2 = feedback_util.create_feedback(s2_token, f2_json)

    f3_json = {
        "comment": "I HATE THIS COURSE AND I'M NEVER TAKING IT AGAIN :(",
        "course": c2,
        "public": True
    }
    f3 = feedback_util.create_feedback(s3_token, f3_json)

    f4_json = {
        "comment": "I haven't taken this course but I just want to let you know it kinda smells here",
        "course": c1,
        "public": False
    }
    f4 = feedback_util.create_feedback(s2_token, f4_json)


def init_app(app):
    app.cli.add_command(auth_test)
    app.cli.add_command(course_test)
    app.cli.add_command(test_all)
    app.cli.add_command(init_data)
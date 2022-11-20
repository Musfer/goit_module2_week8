from datetime import datetime, timedelta
import faker
from random import randint, choice, choices
import sqlite3

NUMBER_GROUPS = 3
NUMBER_GRADES = 20
NUMBER_STUDENTS = 30
NUMBER_SUBJCETS = 5
NUMBER_TEACHERS = 3

START_OF_YEAR = datetime.strptime("2021-09-01", "%Y-%m-%d")
END_OF_YEAR = datetime.strptime("2022-05-31", "%Y-%m-%d")


def generate_date(start: datetime = START_OF_YEAR, end: datetime = END_OF_YEAR) -> list:
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(days=3)
    return choices(result, k=NUMBER_GRADES)


def generate_fake_data() -> tuple:
    students = []
    teachers = []
    subjects = ['calculus', 'linear algebra', 'classical mechanics', 'philosophy', 'statistical physics']
    groups = [x for x in range(1, NUMBER_GROUPS + 1)]
    fake_data = faker.Faker()
    for _ in range(NUMBER_STUDENTS):
        students.append(fake_data.name())
    for _ in range(NUMBER_TEACHERS):
        teachers.append(fake_data.name())
    return students, teachers, groups, subjects


def prepare_data(students, teachers, groups, subjects):
    for_groups = []
    for group in groups:
        for_groups.append((group, ))

    for_teachers = []
    for teacher in teachers:
        for_teachers.append((teacher, ))

    for_students = []
    for student in students:
        for_students.append((student, choice(groups), ))

    for_subjects = []
    for i, subject in enumerate(subjects):
        for_subjects.append((subject, i % NUMBER_TEACHERS + 1, ))

    for_grades = []
    grades = []
    for i, student in enumerate(students):
        for j, subject in enumerate(subjects):
            for date in generate_date():
                grade = randint(40, 100)
                for_grades.append((grade, i+1, j+1, date))

    return for_students, for_teachers, for_groups, for_subjects, for_grades


def insert_data_to_db(students, teachers, groups, subjects, grades):
    with sqlite3.connect('ed.db') as con:
        cur = con.cursor()

        sql_to_students = """INSERT INTO students(fullname, group_id)
                            VALUES (?, ?)"""
        sql_to_groups = """INSERT INTO groups(name)
                            VALUES (?)"""
        sql_to_subjects = """INSERT INTO subjects(name, teacher_id)
                            VALUES (?, ?)"""
        sql_to_teachers = """INSERT INTO teachers(fullname)
                            VALUES (?)"""
        sql_to_grades = """INSERT INTO grades(grade, student_id, subject_id, date_of)
                            VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_students, students)
        cur.executemany(sql_to_subjects, subjects)
        cur.executemany(sql_to_groups, groups)
        cur.executemany(sql_to_teachers, teachers)
        cur.executemany(sql_to_grades, grades)
        con.commit()


if __name__ == '__main__':
    pass
    students, teachers, groups, subjects = generate_fake_data()
    students, teachers, groups, subjects, grades = prepare_data(students, teachers, groups, subjects)
    insert_data_to_db(students, teachers, groups, subjects, grades)

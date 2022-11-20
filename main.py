import sqlite3
from random import choice


def execute_query(sql: str) -> list:
    with sqlite3.connect('ed.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql_subjects = """
SELECT sub.name, sub.id
FROM subjects sub
ORDER BY sub.id ASC
"""
sql_teachers = """
SELECT t.fullname, t.id
FROM teachers t
"""
sql_groups = """
SELECT g.name, g.id
FROM groups g
"""
sql_students = """
SELECT s.fullname, s.id
FROM students s
"""
# 1. 5 студентов с наибольшим средним баллом по всем предметам.
sql1 = """
SELECT s.fullname, round(avg(g.grade), 2) AS avg_grade
FROM grades g
LEFT JOIN students s ON s.id = g.student_id
GROUP BY s.id
ORDER BY avg_grade DESC 
LIMIT 5;
"""

# 2. 1 студент с наивысшим средним баллом по одному предмету.
sql2 = """
SELECT sub.name, s.fullname, round(avg(g.grade), 2) AS avg_grade
from grades g
LEFT JOIN students s ON s.id = g.student_id
LEFT JOIN subjects sub ON sub.id = g.subject_id
WHERE sub.id = %s
GROUP BY s.fullname, sub.name 
ORDER BY avg_grade DESC
LIMIT 1;
"""

# 3. Средний балл в группе по одному предмету.
sql3 = """
SELECT sub.name, round(avg(g.grade), 2) AS avg_grade
from grades g
LEFT JOIN students s ON s.id = g.student_id
LEFT JOIN subjects sub ON sub.id = g.subject_id
LEFT JOIN [groups] gr ON gr.id = s.group_id 
WHERE sub.id = %s AND gr.id = %s
GROUP BY gr.name
ORDER BY avg_grade DESC;
"""

# 4. Средний балл в потоке.
sql4 = """
SELECT round(avg(g.grade), 2) AS avg_grade
from grades g;
"""

# 5. Какие курсы читает преподаватель
sql5 = """
SELECT t.fullname, sub.name
FROM teachers t
LEFT JOIN subjects sub ON t.id = sub.teacher_id 
WHERE t.id = %s
"""

# 6. Список студентов в группе.
sql6 = """
SELECT s.fullname
FROM students s
LEFT JOIN [groups] gr ON s.group_id = gr.id
WHERE gr.id = %s
"""

# 7. Оценки студентов в группе по предмету.
sql7 = """
SELECT stud.fullname, grad.grade 
FROM grades grad
LEFT JOIN students stud ON grad.student_id = stud.id
LEFT JOIN subjects sub ON grad.subject_id = sub.id
LEFT JOIN [groups] gr ON gr.id = stud.group_id
WHERE stud.group_id = %s AND sub.id = %s
"""

# 8. Оценки студентов в группе по предмету на последнем занятии.
sql8 = """
SELECT stud.fullname, grad.grade, grad.date_of 
FROM grades grad
LEFT JOIN students stud ON grad.student_id = stud.id
LEFT JOIN subjects sub ON grad.subject_id = sub.id
LEFT JOIN [groups] gr ON gr.id = stud.group_id
WHERE stud.group_id = %s AND sub.id = %s AND grad.date_of = (
    SELECT grad.date_of
    FROM grades grad
    LEFT JOIN students stud ON grad.student_id = stud.id
    -- LEFT JOIN [groups] gr ON gr.id = drages
    WHERE stud.group_id = %s AND grad.subject_id = %s
    ORDER BY grad.date_of DESC
    LIMIT 1);
"""

# 9. Список курсов, которые посещает студент.
sql9 = """
SELECT sub.name
FROM grades grad 
LEFT JOIN students stud ON stud.id = grad.student_id
LEFT JOIN subjects sub ON grad.subject_id = sub.id
WHERE stud.id = %s
GROUP BY sub.name 
"""

# 10. Список курсов, которые студенту читает преподаватель.
sql10 = """
SELECT sub.name
FROM grades grad 
LEFT JOIN students stud ON stud.id = grad.student_id
LEFT JOIN subjects sub ON grad.subject_id = sub.id
LEFT JOIN teachers t ON sub.teacher_id = t.id
WHERE stud.id = %s AND t.id = %s
GROUP BY sub.name 
"""

# 11. Средний балл, который преподаватель ставит студенту.
sql11 = """
SELECT round(avg(grad.grade), 2) AS avg_grade
FROM grades grad 
LEFT JOIN students stud ON stud.id = grad.student_id
LEFT JOIN subjects sub ON grad.subject_id = sub.id
LEFT JOIN teachers t ON sub.teacher_id = t.id
WHERE t.id = %s AND stud.id = %s
"""

# 12. Средний балл, который ставит преподаватель.
sql12 = """
SELECT round(avg(grad.grade), 2) AS avg_grade
FROM grades grad 
LEFT JOIN subjects sub ON grad.subject_id = sub.id
LEFT JOIN teachers t ON sub.teacher_id = t.id
WHERE t.id = %s
"""


if __name__ == '__main__':
    subjects = {}
    for x in execute_query(sql_subjects):
        subjects[x[0]] = x[1]
    print(f'list of subjects with id: {subjects}')
    teachers = {}
    for x in execute_query(sql_teachers):
        teachers[x[0]] = x[1]
    print(f'list of teachers with id: {teachers}')
    groups = {}
    for x in execute_query(sql_groups):
        groups[x[0]] = x[1]
    print(f'list of groups with id: {groups}')
    students = {}
    for x in execute_query(sql_students):
        students[x[0]] = x[1]
    print(f'list of students with id: {students}')
    print('\n')


    #  random choice of teacher, subject, and group
    subject = choice([x for x in subjects.keys()])  # number of subject from subjects list 1 to 5
    subject_id = subjects.get(subject)
    group = choice([x for x in groups.keys()])  # number of group from 1 to 3
    group_id = groups.get(group)
    teacher = choice([x for x in teachers.keys()])  # number of teacher from teachers list from 1 to 3
    teacher_id = teachers.get(teacher)
    student = choice([x for x in students.keys()])
    student_id = students.get(student)

    #  subjects = ['calculus', 'linear algebra', 'classical mechanics', 'philosophy', 'statistical physics']
    print('TASK 1:' + ' 5 студентов с наибольшим средним баллом по всем предметам.')
    print(execute_query(sql1), '\n')

    print('TASK 2:' + f' студент с наивысшим средним баллом по предмету {subject}.')
    print(execute_query(sql2 % subject_id), '\n')

    print('TASK 3:' + f' средний балл в {group} группе по предмету {subject}.')
    print(execute_query(sql3 % (subject_id, group_id)), '\n')

    print('TASK 4:' + f' средний балл в потоке.')
    print(execute_query(sql4)[0][0], '\n')

    print('TASK 5:' + f' какие курсы читает преподаватель {teacher}')
    print(execute_query(sql5 % teacher_id), '\n')

    print('TASK 6:' + f' cписок студентов в {group} группе.')
    print([x[0] for x in execute_query(sql6 % group_id)], '\n')

    print('TASK 7:' + f' оценки студентов {group} группы по предмету {subject}.')
    print(execute_query(sql7 % (group_id, subject_id)), '\n')

    print('TASK 8:' + f' оценки студентов {group} группы по предмету {subject} на последнем занятии.')
    print(execute_query(sql8 % (group_id, subject_id, group_id, subject_id)), '\n')

    print('TASK 9:' + f' cписок курсов, которые посещает студент {student}.')
    print([x[0] for x in execute_query(sql9 % student_id)], '\n')

    print('TASK 10:' + f' cписок курсов, которые студенту {student} читает преподаватель {teacher}.')
    print([x[0] for x in execute_query(sql10 % (student_id, teacher_id))], '\n')

    print('TASK 11:' + f' cредний балл, который преподаватель {teacher} ставит студенту {student}.')
    print(execute_query(sql11 % (teacher_id, student_id))[0][0], '\n')

    print('TASK 12:' + f' cредний балл, который ставит преподаватель {teacher}.')
    print(execute_query(sql12 % teacher_id)[0][0], '\n')

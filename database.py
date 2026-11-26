import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YourNewPassword123!",
        database="student_study_planner"
    )

def get_courses():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Courses")
    courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return courses

def get_assignments(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            Assignments.assignment_id,
            Assignments.assignment_name,
            Assignments.description,
            Assignments.due_date,
            Assignments.status,
            Courses.course_name,
            Courses.course_code,
            Courses.course_id
        FROM Assignments
        JOIN Courses
        ON Assignments.course_id = Courses.course_id
        WHERE Assignments.user_id = %s
        ORDER BY Assignments.due_date ASC
    """

    cursor.execute(query, (user_id,))
    assignments = cursor.fetchall()

    for assignment in assignments:
        assignment["due_date"] = assignment["due_date"].isoformat()

    cursor.close()
    connection.close()

    return assignments

def add_assignment(user_id, name, description, due_date, course_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO Assignments
        (assignment_name, description, due_date, course_id, user_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (name, description, due_date, course_id, user_id)
    )

    connection.commit()

    cursor.close()
    connection.close()

def update_assignment(user_id, assignment_id, name, description, due_date, course_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE Assignments
        SET assignment_name = %s,
            description = %s,
            due_date = %s,
            course_id = %s
        WHERE assignment_id = %s AND user_id = %s
    """

    cursor.execute(
        query,
        (name, description, due_date, course_id, assignment_id, user_id)
    )

    connection.commit()
    updated = cursor.rowcount > 0

    cursor.close()
    connection.close()

    return updated

def delete_assignment(user_id, assignment_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM Assignments WHERE assignment_id = %s AND user_id = %s",
        (assignment_id, user_id)
    )

    connection.commit()
    deleted = cursor.rowcount > 0

    cursor.close()
    connection.close()

    return deleted

def complete_assignment(user_id, assignment_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE Assignments
        SET status = 'Completed'
        WHERE assignment_id = %s AND user_id = %s
        """,
        (assignment_id, user_id)
    )

    connection.commit()
    updated = cursor.rowcount > 0

    cursor.close()
    connection.close()

    return updated
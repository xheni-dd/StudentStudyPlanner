from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from functools import wraps
import database

app = Flask(__name__)

# Change this to a long, random secret before using the app publicly.
app.secret_key = "replace-this-with-a-long-random-secret"

# CHECK IF USER IS LOGGED IN
def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            if request.path.startswith("/api/"):
                return jsonify({"error": "Please log in first."}), 401
            return redirect(url_for("login"))

        return function(*args, **kwargs)

    return wrapper

# LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        connection = database.get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT * FROM Users WHERE email = %s",
                (email,)
            )
            user = cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

        if user and user["password_hash"] == password:
            session["user_id"] = user["user_id"]
            session["first_name"] = user["first_name"]

            return redirect(url_for("home"))

        flash("Incorrect email or password.")

    return render_template("login.html")

# REGISTER PAGE
@app.route("/register", methods=["POST"])
def register():
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not first_name or not last_name or not email or not password:
        flash("Please fill in all fields.")
        return redirect(url_for("login"))

    if len(password) < 8:
        flash("Your password must have at least 8 characters.")
        return redirect(url_for("login"))

    connection = database.get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO Users
            (first_name, last_name, email, password_hash)
            VALUES (%s, %s, %s, %s)
            """,
            (first_name, last_name, email, password)
        )

        connection.commit()
        flash("Account created! You can now log in.")

    except Exception:
        connection.rollback()
        flash("This email may already be registered. Try another one.")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("login"))

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# MAIN WEBSITE
@app.route("/")
@login_required
def home():
    return render_template("index.html")

# GET COURSES AND THIS USER'S ASSIGNMENTS
@app.route("/api/dashboard", methods=["GET"])
@login_required
def dashboard():
    try:
        assignments = database.get_assignments(session["user_id"])
        courses = database.get_courses()

        return jsonify({
            "assignments": assignments,
            "courses": courses
        })

    except Exception as error:
        return jsonify({"error": str(error)}), 500

# ADD ASSIGNMENT
@app.route("/api/assignments", methods=["POST"])
@login_required
def add_assignment():
    data = request.get_json() or {}

    name = data.get("assignment_name", "").strip()
    description = data.get("description", "")
    due_date = data.get("due_date")
    course_id = data.get("course_id")

    if not name or not due_date or not course_id:
        return jsonify({"error": "Please fill in all required fields."}), 400

    try:
        database.add_assignment(
            session["user_id"], name, description, due_date, int(course_id)
        )

        return jsonify({"message": "Assignment added successfully!"}), 201

    except Exception as error:
        return jsonify({"error": str(error)}), 500

# EDIT ASSIGNMENT
@app.route("/api/assignments/<int:assignment_id>", methods=["PUT"])
@login_required
def edit_assignment(assignment_id):
    data = request.get_json() or {}

    name = data.get("assignment_name", "").strip()
    description = data.get("description", "")
    due_date = data.get("due_date")
    course_id = data.get("course_id")

    if not name or not due_date or not course_id:
        return jsonify({"error": "Please fill in all required fields."}), 400

    try:
        updated = database.update_assignment(
            session["user_id"],
            assignment_id,
            name,
            description,
            due_date,
            int(course_id)
        )

        if not updated:
            return jsonify({"error": "Assignment not found."}), 404

        return jsonify({"message": "Assignment updated successfully!"})

    except Exception as error:
        return jsonify({"error": str(error)}), 500

# DELETE ASSIGNMENT
@app.route("/api/assignments/<int:assignment_id>", methods=["DELETE"])
@login_required
def remove_assignment(assignment_id):
    try:
        deleted = database.delete_assignment(session["user_id"], assignment_id)

        if not deleted:
            return jsonify({"error": "Assignment not found."}), 404

        return jsonify({"message": "Assignment deleted successfully!"})

    except Exception as error:
        return jsonify({"error": str(error)}), 500

# MARK ASSIGNMENT AS COMPLETED
@app.route("/api/assignments/<int:assignment_id>/complete", methods=["PATCH"])
@login_required
def mark_completed(assignment_id):
    try:
        updated = database.complete_assignment(session["user_id"], assignment_id)

        if not updated:
            return jsonify({"error": "Assignment not found."}), 404

        return jsonify({"message": "Assignment completed!"})

    except Exception as error:
        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run(debug=True)
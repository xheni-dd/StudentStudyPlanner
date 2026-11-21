
from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)


# Open the main website
@app.route("/")
def home():
    return render_template("index.html")


# Get courses and assignments
@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    try:
        assignments = database.get_assignments()
        courses = database.get_courses()

        return jsonify({
            "assignments": assignments,
            "courses": courses
        })
    except Exception as error:
        return jsonify({"error": str(error)}), 500


# Add a new assignment
@app.route("/api/assignments", methods=["POST"])
def add_assignment():
    data = request.get_json()

    name = data.get("assignment_name", "").strip()
    description = data.get("description", "")
    due_date = data.get("due_date")
    course_id = data.get("course_id")

    if not name or not due_date or not course_id:
        return jsonify({"error": "Please fill in all required fields."}), 400

    try:
        database.add_assignment(
            name, description, due_date, int(course_id)
        )

        return jsonify({"message": "Assignment added successfully!"}), 201

    except Exception as error:
        return jsonify({"error": str(error)}), 500


# Edit an assignment
@app.route("/api/assignments/<int:assignment_id>", methods=["PUT"])
def edit_assignment(assignment_id):
    data = request.get_json()

    name = data.get("assignment_name", "").strip()
    description = data.get("description", "")
    due_date = data.get("due_date")
    course_id = data.get("course_id")

    if not name or not due_date or not course_id:
        return jsonify({"error": "Please fill in all required fields."}), 400

    try:
        database.update_assignment(
            assignment_id,
            name,
            description,
            due_date,
            int(course_id)
        )

        return jsonify({"message": "Assignment updated successfully!"})

    except Exception as error:
        return jsonify({"error": str(error)}), 500


# Delete an assignment
@app.route("/api/assignments/<int:assignment_id>", methods=["DELETE"])
def remove_assignment(assignment_id):
    try:
        database.delete_assignment(assignment_id)

        return jsonify({"message": "Assignment deleted successfully!"})

    except Exception as error:
        return jsonify({"error": str(error)}), 500


# Mark assignment as completed
@app.route("/api/assignments/<int:assignment_id>/complete", methods=["PATCH"])
def mark_completed(assignment_id):
    try:
        database.complete_assignment(assignment_id)

        return jsonify({"message": "Assignment completed!"})

    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(debug=True)

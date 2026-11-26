let assignments = [];
let courses = [];

const form = document.getElementById("assignment-form");
const nameInput = document.getElementById("assignment-name");
const courseInput = document.getElementById("course");
const dateInput = document.getElementById("due-date");
const descriptionInput = document.getElementById("description");
const assignmentIdInput = document.getElementById("assignment-id");

const saveButton = document.getElementById("save-button");
const cancelButton = document.getElementById("cancel-button");
const formTitle = document.getElementById("form-title");
const message = document.getElementById("message");


// LOAD DASHBOARD DATA

async function loadDashboard() {
    try {
        const response = await fetch("/api/dashboard");

        if (!response.ok) {
            throw new Error("Could not load dashboard.");
        }

        const data = await response.json();

        assignments = data.assignments;
        courses = data.courses;

        displayCourses();
        displayDashboard();

    } catch (error) {
        showMessage(error.message);
    }
}


// DISPLAY COURSES

function displayCourses() {
    courseInput.innerHTML = '<option value="">Select a course</option>';

    courses.forEach(course => {
        const option = document.createElement("option");

        option.value = course.course_id;
        option.textContent =
            course.course_code + " - " + course.course_name;

        courseInput.appendChild(option);
    });
}


// ADD OR EDIT ASSIGNMENT

form.addEventListener("submit", async function(event) {
    event.preventDefault();

    const assignment = {
        assignment_name: nameInput.value.trim(),
        course_id: courseInput.value,
        due_date: dateInput.value,
        description: descriptionInput.value.trim()
    };

    if (!assignment.assignment_name ||
        !assignment.course_id ||
        !assignment.due_date) {
        showMessage("Please fill in all required fields.");
        return;
    }

    const id = assignmentIdInput.value;

    const url = id
        ? `/api/assignments/${id}`
        : "/api/assignments";

    const method = id ? "PUT" : "POST";

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(assignment)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Something went wrong.");
        }

        showMessage(result.message);

        resetForm();
        await loadDashboard();

    } catch (error) {
        showMessage(error.message);
    }
});


// EDIT ASSIGNMENT

function editAssignment(id) {
    const assignment = assignments.find(
        item => item.assignment_id === id
    );

    if (!assignment) return;

    if (assignment.status === "Completed") {
        showMessage("Completed assignments cannot be edited.");
        return;
    }

    assignmentIdInput.value = assignment.assignment_id;
    nameInput.value = assignment.assignment_name;
    courseInput.value = assignment.course_id;
    dateInput.value = assignment.due_date;
    descriptionInput.value = assignment.description || "";

    formTitle.textContent = "Edit Assignment";
    saveButton.textContent = "Update Assignment";
    cancelButton.hidden = false;

    window.scrollTo({ top: 0, behavior: "smooth" });
}


// RESET FORM

function resetForm() {
    form.reset();
    assignmentIdInput.value = "";

    formTitle.textContent = "Add New Assignment";
    saveButton.textContent = "Add Assignment";
    cancelButton.hidden = true;
}

cancelButton.addEventListener("click", resetForm);


// DELETE ASSIGNMENT

async function deleteAssignment(id) {
    if (!confirm("Are you sure you want to delete this assignment?")) {
        return;
    }

    try {
        const response = await fetch(`/api/assignments/${id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not delete assignment.");
        }

        showMessage(result.message);
        await loadDashboard();

    } catch (error) {
        showMessage(error.message);
    }
}


// MARK AS COMPLETED

async function completeAssignment(id) {
    try {
        const response = await fetch(
            `/api/assignments/${id}/complete`,
            { method: "PATCH" }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not update assignment.");
        }

        showMessage(result.message);
        await loadDashboard();

    } catch (error) {
        showMessage(error.message);
    }
}

// DASHBOARD DISPLAY

function displayDashboard() {
    const dueSoonList = document.getElementById("due-soon-list");
    const upcomingList = document.getElementById("upcoming-list");
    const completedList = document.getElementById("completed-list");
    const missedList = document.getElementById("missed-list");

    dueSoonList.innerHTML = "";
    upcomingList.innerHTML = "";
    completedList.innerHTML = "";
    missedList.innerHTML = "";

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    assignments.forEach(assignment => {
        const dueDate = new Date(assignment.due_date + "T00:00:00");

        const daysLeft = Math.round(
            (dueDate - today) / (1000 * 60 * 60 * 24)
        );

        if (assignment.status === "Completed") {
            createAssignmentCard(assignment, completedList);
        }

        else if (daysLeft < 0) {
            createAssignmentCard(assignment, missedList);
        }

        else if (daysLeft <= 7) {
            createAssignmentCard(assignment, dueSoonList);
        }

        else {
            createAssignmentCard(assignment, upcomingList);
        }
    });

    showEmptyMessage(dueSoonList);
    showEmptyMessage(upcomingList);
    showEmptyMessage(completedList);
    showEmptyMessage(missedList);

    updateProgress();
}

// CREATE ASSIGNMENT CARD

function createAssignmentCard(assignment, container) {
    const card = document.createElement("div");
    card.className = "assignment-card";

    if (container.id === "completed-list") {
        card.classList.add("completed-card");
    }
    else if (container.id === "due-soon-list") {
        card.classList.add("due-soon-card");
    }
    else if (container.id === "missed-list") {
    card.classList.add("missed-card");
    }

    const title = document.createElement("h3");
    title.textContent = assignment.assignment_name;

    const course = document.createElement("p");
    course.textContent =
        "Course: " + assignment.course_name;

    const date = document.createElement("p");
    date.textContent =
        "Due Date: " + assignment.due_date;

    const description = document.createElement("p");
    description.textContent =
        "Description: " + (assignment.description || "None");

    const status = document.createElement("p");
    status.textContent = "Status: " + assignment.status;

    card.append(title, course, date, description, status);

    if (assignment.status === "Pending") {
        const actions = document.createElement("div");
        actions.className = "assignment-actions";

        const editButton = document.createElement("button");
        editButton.textContent = "Edit";
        editButton.addEventListener("click", () => {
            editAssignment(assignment.assignment_id);
        });

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.className = "delete-button";
        deleteButton.addEventListener("click", () => {
            deleteAssignment(assignment.assignment_id);
        });

        const completeButton = document.createElement("button");
        completeButton.textContent = "Mark Completed";
        completeButton.className = "complete-button";
        completeButton.addEventListener("click", () => {
            completeAssignment(assignment.assignment_id);
        });

        actions.append(editButton, deleteButton, completeButton);
        card.appendChild(actions);
    }

    container.appendChild(card);
}


// EMPTY SECTION MESSAGE

function showEmptyMessage(container) {
    if (container.children.length === 0) {
        const empty = document.createElement("p");
        empty.className = "empty-message";
        empty.textContent = "No assignments in this section.";

        container.appendChild(empty);
    }
}


// PROGRESS BAR

function updateProgress() {
    const total = assignments.length;

    const completed = assignments.filter(
        item => item.status === "Completed"
    ).length;

    let percentage = 0;

    if (total > 0) {
        percentage = Math.round((completed / total) * 100);
    }

    document.getElementById("progress-fill").style.width =
        percentage + "%";

    document.getElementById("progress-text").textContent =
        percentage + "% Completed (" +
        completed + " of " + total + " assignments)";
}


// DISPLAY MESSAGES

function showMessage(text) {
    message.textContent = text;
}


// START WEBSITE

loadDashboard();

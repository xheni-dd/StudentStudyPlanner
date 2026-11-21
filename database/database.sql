CREATE DATABASE student_study_planner;

USE student_study_planner;

-- Courses table
CREATE TABLE Courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(20)
);

-- Assignments table
CREATE TABLE Assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    assignment_name VARCHAR(150) NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,
    status ENUM('Pending', 'Completed') DEFAULT 'Pending',
    course_id INT NOT NULL,
    FOREIGN KEY (course_id)
        REFERENCES Courses(course_id)
        ON DELETE CASCADE
);


-- Sample courses
INSERT INTO courses (course_name, course_code)
VALUES
('Calculus I', 'MTH 229'),
('Calculus II', 'MTH 230'),
('Statistics', 'MTH 250'),
('College Algebra', 'MTH 120'),
('Discrete Mathematics', 'MTH 310'),
('Introduction to Programming', 'CSC 126'),
('Computer Science I', 'CSC 211'),
('Computer Science II', 'CSC 212'),
('Web Database Applications', 'CSC 226'),
('Data Structures', 'CSC 315'),
('Database Management', 'CSC 332'),
('Cybersecurity Fundamentals', 'CSC 300'),
('Network Security', 'CSC 421'),
('Cryptography', 'CSC 426'),
('Information Systems', 'ISI 300'),
('Systems Analysis', 'ISI 310'),
('Information Technology', 'ISI 200'),
('Business Management', 'MGT 200'),
('Principles of Management', 'MGT 210'),
('Marketing', 'MKT 200'),
('Accounting I', 'ACC 101'),
('Accounting II', 'ACC 102'),
('Microeconomics', 'ECO 101'),
('Macroeconomics', 'ECO 102'),
('Business Statistics', 'BUS 250'),
('English Composition', 'ENG 111'),
('Public Speaking', 'COM 101'),
('Italian I', 'ITA 101'),
('Psychology', 'PSY 101'),
('Introduction to Sociology', 'SOC 101');
CREATE DATABASE lms_db;

USE lms_db;

CREATE TABLE courses (
    course_id VARCHAR(6) PRIMARY KEY,
    name VARCHAR(100)
);

select * from courses;
drop table courses;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enrollment_no VARCHAR(12),
    name VARCHAR(100)
);


CREATE TABLE instructors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    faculty_id varchar(15),
    name VARCHAR(100)
);

SELECT * from instructors, courses, students;

drop table instructors, students, courses

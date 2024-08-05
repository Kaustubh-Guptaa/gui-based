CREATE DATABASE prog6_db;

USE prog6_db;

CREATE TABLE code_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    version INT NOT NULL,
    change_description TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_path VARCHAR(255) NOT NULL
);

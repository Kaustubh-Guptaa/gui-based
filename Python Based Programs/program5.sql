CREATE DATABASE prog5_db;

USE prog5_db;

CREATE TABLE notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO notes (title, content, file_path) VALUES
('Meeting Notes', 'Discussed project requirements and timelines.', '/program5/meeting_notes.txt'),
('Shopping List', 'Milk, Eggs, Bread, Butter', '/program5/shopping_list.txt'),
('Ideas', 'Brainstorming for new product features.', '/program5/ideas.txt');

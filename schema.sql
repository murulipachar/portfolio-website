CREATE DATABASE IF NOT EXISTS portfolio_cms;
USE portfolio_cms;

CREATE TABLE IF NOT EXISTS admins(
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50),
  email VARCHAR(100) UNIQUE,
  password VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS sections(
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) UNIQUE,
  content TEXT
);

CREATE TABLE IF NOT EXISTS skills(
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  level INT
);

CREATE TABLE IF NOT EXISTS projects(
  id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(200),
  short_desc VARCHAR(255),
  description TEXT,
  tech_stack VARCHAR(255),
  github_link VARCHAR(255),
  live_link VARCHAR(255),
  created_at DATETIME
);

CREATE TABLE IF NOT EXISTS messages(
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  email VARCHAR(100),
  message TEXT,
  created_at DATETIME
);

-- Create default admin (email: admin@example.com, password: admin123)
INSERT INTO admins (name, email, password)
VALUES (
  'Admin',
  'admin@example.com',
  '$pbkdf2-sha256$600000$placeholder$placeholderhash'
)
ON DUPLICATE KEY UPDATE email=email;

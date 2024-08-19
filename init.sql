-- Create the employee table
CREATE TABLE IF NOT EXISTS employee (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  city VARCHAR(100)
);

-- Insert 10 random rows into the employee table
INSERT INTO employee (name, city) VALUES
('John Doe', 'New York'),
('Jane Smith', 'Los Angeles'),
('Michael Johnson', 'Houston'),
('Emily Davis', 'Houston'),
('Daniel Wilson', 'Phoenix'),
('Matthew Brown', 'Houston'),
('Sophia Martinez', 'San Antonio'),
('Olivia Garcia', 'San Diego'),
('Elijah Anderson', 'Phoenix'),
('Ava Thomas', 'Los Angeles');

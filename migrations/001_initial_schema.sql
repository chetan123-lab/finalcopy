-- Placeholder migration script
-- This is a sample database migration that would be run during deployment
-- In a real application, this might create tables, indexes, or modify the schema

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (username, email) 
VALUES ('admin', 'admin@example.com')
ON CONFLICT (username) DO NOTHING;
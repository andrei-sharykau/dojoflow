-- Create dojoflow user with password
CREATE USER dojoflow WITH PASSWORD 'dojoflowpassword';

-- Grant privileges to dojoflow user
GRANT ALL PRIVILEGES ON DATABASE dojoflow TO dojoflow;

-- Connect to dojoflow database
\c dojoflow

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO dojoflow; 
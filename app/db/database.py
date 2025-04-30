import sqlite3  # For working with SQLite database
from datetime import datetime  # For handling dates and times
import pytz  # For timezone handling

# Initialize the database (creates it if it doesn't exist)
def init_db():
    """Creates the database and checks if the 'users' table exists. If not, it creates it."""
    conn = sqlite3.connect("users.db")  
    cur = conn.cursor() 
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY, 
            username TEXT,  
            last_seen TEXT  
        )
    ''')

    # Check if the "last_seen" column exists, if not, add it
    cur.execute('PRAGMA table_info(users);')  # Get the structure of the "users" table
    columns = cur.fetchall()  # Fetch all columns
    if not any(col[1] == 'last_seen' for col in columns):  # If "last_seen" column is missing
        cur.execute('ALTER TABLE users ADD COLUMN last_seen TEXT;')  # Add the missing column

    conn.commit()  # Save (commit) changes
    conn.close()  # Close the database connection

# Add a new user or update the existing user's information
def add_user(user_id, username, timestamp):
    """Adds a user to the database or updates the user's information."""
    conn = sqlite3.connect("users.db")  # Connect to the database
    cur = conn.cursor()  # Create a cursor object

    # Insert a new user or update if user_id already exists
    cur.execute('''
        INSERT INTO users (user_id, username, last_seen)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET  
            username = excluded.username,
            last_seen = excluded.last_seen
    ''', (user_id, username, timestamp))  

    conn.commit()  # Commit changes to the database
    conn.close()  # Close the connection

# Fetch all users from the database
def get_all_users():
    """Fetches all users' data from the database."""
    conn = sqlite3.connect("users.db")  # Connect to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute("SELECT * FROM users")  # Fetch all records from the users table
    rows = cur.fetchall()  # Get all rows
    conn.close()  # Close the connection
    return rows  # Return the list of all users

# Fetch a specific user's data by user_id
def get_user(user_id):
    """Fetches data for a specific user based on their user_id."""
    conn = sqlite3.connect("users.db")  # Connect to the database
    cur = conn.cursor()  # Create a cursor object
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))  # Fetch user by ID
    user = cur.fetchone()  # Fetch the first (and only) matching result
    conn.close()  # Close the connection
    return user  # Return the user's data
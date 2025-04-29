import sqlite3  # For working with SQLite database
from datetime import datetime  # For handling dates and times
import pytz  # For timezone handling

# Initialize the database (creates it if it doesn't exist)
def init_db():
    """Creates the database and checks if the 'users' table exists. If not, it creates it."""
    conn = sqlite3.connect("users.db")  # Connect to the SQLite database
    cur = conn.cursor()  # Create a cursor to interact with the database
    # Create the 'users' table if it doesn't already exist
    # The user's unique ID
    # The user's name
    # The last seen timestamp
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY, 
            username TEXT,  
            last_seen TEXT  
        )
    ''')

    # Check if the "last_seen" column exists, if not, add it
    cur.execute('PRAGMA table_info(users);')  # Get the table structure
    columns = cur.fetchall()  # Fetch the table structure
    if not any(col[1] == 'last_seen' for col in columns):  # Check if "last_seen" column is missing
        cur.execute('ALTER TABLE users ADD COLUMN last_seen TEXT;')  # Add the "last_seen" column

    conn.commit()  # Commit the changes
    conn.close()  # Close the connection

# Add a new user or update the existing user's information
def add_user(user_id, username):
    """Adds a user to the database or updates the user's information."""
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    # Get the current time in Azerbaijan's timezone
    az_timezone = pytz.timezone("Asia/Baku")  # Set the timezone to Azerbaijan
    az_time = datetime.now(az_timezone)  # Get the current time in Azerbaijan's timezone
    formatted_time = az_time.strftime("%d.%m.%Y %H:%M")  # Format the time in a readable format

    # Insert the new user or update the existing user's information
    # If user exists, update their info
    cur.execute('''
        INSERT INTO users (user_id, username, last_seen)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET  
            username = excluded.username,
            last_seen = excluded.last_seen
    ''', (user_id, username, formatted_time))  # Insert or update data

    conn.commit()  # Commit the changes
    conn.close()  # Close the connection

# Additional functions:
# - Function to get all users from the database
def get_all_users():
    """Fetches all users' data from the database."""
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")  # Select all users
    rows = cur.fetchall()  # Fetch all rows
    conn.close()  # Close the connection
    return rows  # Return all users

# - Function to get a specific user's data by user_id
def get_user(user_id):
    """Fetches data for a specific user based on their user_id."""
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))  # Fetch user by ID
    user = cur.fetchone()  # Fetch the user data
    conn.close()  # Close the connection
    return user  # Return the user's data
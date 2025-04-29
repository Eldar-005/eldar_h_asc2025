from dotenv import load_dotenv  # To load environment variables from a .env file
import os  # For working with environment variables
from bot import MyClient  # Importing the MyClient class, which is your custom Discord client
import discord  # Importing discord.py library to interact with Discord's API

# Load environment variables from the .env file
load_dotenv()

# Create the necessary intents for the bot
intents = discord.Intents.default()  # Default intents are a basic set of permissions for the bot
intents.message_content = True  # Allow the bot to access the content of messages

# Initialize the client with the intents (providing the necessary permissions for the bot to work properly)
client = MyClient(intents=intents)

# Run the bot using the Discord token retrieved from the environment variables
client.run(os.getenv("DISCORD_TOKEN"))
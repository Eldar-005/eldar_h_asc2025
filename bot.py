import os  # For accessing environment variables
import discord  # Main library for creating a Discord bot
import json  # For handling JSON data
import random  # For selecting random quotes
from dotenv import load_dotenv  # For loading environment variables from .env file
from app.ai.hf_ai import hf_response  # Import AI response generation function
from app.db.database import init_db, add_user  # Import database functions

load_dotenv()  # Load environment variables from .env
init_db()  # Initialize the database (creates necessary tables if they do not exist)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # Fetch Discord bot token from environment

# Global user language preferences (stores user language settings)
user_langs = {}

def load_quotes():
    """Load quotes from the JSON file."""
    with open("app/quotes/quotes.json", "r", encoding="utf-8") as file:
        return json.load(file)

quotes_data = load_quotes()  # Load the quotes at the start

def get_quote_from_json(topic, lang="en"):
    """Fetch a random quote from the JSON file based on the topic and language."""
    matching_quotes = [q["quote"] for q in quotes_data if q["topic"] == topic and q["lang"] == lang]
    if not matching_quotes:
        return None  # If no matching quote, return None
    return random.choice(matching_quotes)  # Return a random quote

class MyClient(discord.Client):
    """Custom client class for handling Discord bot events."""
    
    async def on_ready(self):
        """Event triggered when the bot successfully connects to Discord."""
        print(f"[OK] Logged in as {self.user}")  # Log bot's username

    async def on_message(self, message):
        """Event triggered whenever a message is sent to the server."""
        if message.author == self.user:  # Ignore bot's own messages
            return

        add_user(str(message.author.id), str(message.author))  # Add user to the database if not already

        content = message.content.strip()  # Clean the message content

        # Command to change language
        if content.startswith("/lang"):
            parts = content.split(" ")
            if len(parts) > 1 and parts[1] in ["az", "en"]:  # Check if language is valid
                user_langs[str(message.author.id)] = parts[1]  # Set user language preference
                await message.channel.send(f"🌐 Dil seçildi: `{parts[1]}`")  # Acknowledge language change
            else:
                await message.channel.send("⚠️ İstifadə: `/lang az` və ya `/lang en`")  # Incorrect command format
            return

        # Command to fetch a citation
        if content.startswith("/cite"):
            parts = content.split(" ", 1)
            if len(parts) < 2:
                await message.channel.send("⚠️ İstifadə: `/cite mövzu` (məsələn: `/cite life`)")  # Missing topic
                return

            topic = parts[1].strip().lower()  # Get the topic of the citation
            lang = user_langs.get(str(message.author.id), "en")  # Get user language, default is "en"

            try:
                # First try fetching from AI
                ai_quote = hf_response(topic, mode="quote")
                if ai_quote and "error" not in ai_quote.lower():  # If AI provides a valid quote
                    await message.channel.send(f"🤖 AI sitatı:\n{ai_quote}")
                else:
                    raise Exception("AI quote not available")  # If AI fails, fallback to JSON quotes
            except:
                # Fallback to local quotes if AI fails
                local_quote = get_quote_from_json(topic, lang)
                if local_quote:
                    await message.channel.send(f"📜 JSON sitatı:\n{local_quote}")  # Send JSON quote
                else:
                    await message.channel.send("❌ Sitat tapılmadı.")  # If no quote is found

            return

        # AI-style chat response command
        if content.startswith(("/ai", "/bot", "/chatgpt")):
            parts = content.split(" ", 2)
            style = parts[1] if len(parts) > 2 else None  # Get the style (if provided)
            prompt = parts[2] if len(parts) > 2 else parts[1] if len(parts) > 1 else ""  # Get the prompt

            if not prompt:  # If no prompt is provided, request one from the user
                await message.channel.send("⚠️ Please provide a message.")
                return

            try:
                # Try to generate a response from AI
                response = hf_response(prompt, style, mode="chat")
                await message.channel.send(f"💬 Answer: {response}")  # Send AI's response
            except Exception as e:
                await message.channel.send(f"❌ Error: {e}")  # Handle error and send error message

# Create bot client with necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Ensure bot can read message content

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)  # Start the bot with the provided Discord token
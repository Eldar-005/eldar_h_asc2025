from app.ai.hf_ai import hf_response  
from app.db.database import init_db, add_user
import discord
import json
import random
import os
from dotenv import load_dotenv
from datetime import datetime
import pytz  # For timezone handling

load_dotenv()
init_db()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
user_langs = {}  # Dictionary to store user language preferences

# Load quotes from local JSON file
def load_quotes():
    with open("app/quotes/quotes.json", "r", encoding="utf-8") as file:
        return json.load(file)

quotes_data = load_quotes()

# Get a quote from JSON file based on topic and language
def get_quote_from_json(topic, lang="en"):
    matching_quotes = [q["quote"] for q in quotes_data if q["topic"] == topic and q["lang"] == lang]
    if not matching_quotes:
        return None
    return random.choice(matching_quotes)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"[OK] Logged in as {self.user}")

    async def on_message(self, message):
        """Event triggered whenever a message is sent to the server."""
        if message.author == self.user:  # Ignore bot's own messages
            return

        # Get the current timestamp in Asia/Baku timezone
        timestamp = datetime.now(pytz.timezone("Asia/Baku")).strftime("%d.%m.%Y %H:%M")

        # Add user to the database with timestamp
        add_user(str(message.author.id), str(message.author), timestamp)

        content = message.content.strip()  # Clean message content

        # Command to change language
        if content.startswith("/lang"):
            parts = content.split(" ")
            if len(parts) > 1 and parts[1] in ["az", "en"]:  # Check if language code is valid
                user_langs[str(message.author.id)] = parts[1]  # Save user's preferred language
                await message.channel.send(f"🌐 Language set to: `{parts[1]}`")
            else:
                await message.channel.send("⚠️ Usage: `/lang az` or `/lang en`")
            return

        # Command to fetch a quote
        if content.startswith("/cite"):
            parts = content.split(" ", 1)
            if len(parts) < 2:
                await message.channel.send("⚠️ Usage: `/cite topic` (e.g. `/cite life`)")
                return

            topic = parts[1].strip().lower()  # Extract topic
            lang = user_langs.get(str(message.author.id), "en")  # Get preferred language or default to English

            try:
                # First try to get AI-generated quote
                ai_quote = hf_response(topic, mode="quote", lang=lang)
                if ai_quote and "error" not in ai_quote.lower() and ai_quote != "i was a success /lang az":
                    await message.channel.send(f"🤖 AI quote:\n{ai_quote}")
                else:
                    raise Exception("AI failed to provide a valid quote")
            except Exception as e:
                # If AI fails, fallback to local JSON quote
                print(f"AI error: {e}")
                local_quote = get_quote_from_json(topic, lang)
                if local_quote:
                    await message.channel.send(f"📜 JSON quote:\n{local_quote}")
                else:
                    await message.channel.send("❌ Quote not found.")

            return

        # AI-style chat response command
        if content.startswith(("/ai", "/bot", "/chatgpt")):
            parts = content.split(" ", 2)
            if len(parts) < 2:
                await message.channel.send("⚠️ Please provide a prompt after the command.")
                return

            style = parts[1] if len(parts) > 2 else None  # Optional style
            prompt = parts[2] if len(parts) > 2 else parts[1]  # The prompt itself

            if not prompt:
                await message.channel.send("⚠️ Please provide a message.")
                return

            try:
                # Generate AI response
                response = hf_response(prompt, style, mode="chat")
                await message.channel.send(f"💬 Response: {response}")
            except Exception as e:
                await message.channel.send(f"❌ Error: {e}")


# Set required intents
intents = discord.Intents.default()
intents.message_content = True

# Create and run the bot client
client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)
# eh_bot - Discord AI Bot

A lightweight, intelligent Discord bot with AI-powered chat and quote generation. Built for the ADA School AI Challenge 2025 competition.

## 🚀 Features

- 🤖 Ask the bot anything using `/ai`, `/chatgpt`, or `/bot`
- 🎭 Choose different response styles (kid, teacher, robot, poet, etc.)
- 🧠 Get smart AI-generated quotes with `/cite [topic]`
- 🌐 Switch bot response language with `/lang az` or `/lang en`
- 🗃️ Stores users and last seen time using SQLite
- 🔐 Secure API key usage via `.env`
- 💡 Local fallback quotes from `quotes.json` when AI is not available

## 🛠️ Tech Stack

- Python
- Discord API (discord.py)
- Hugging Face Inference API
- SQLite3
- dotenv

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Eldar-005/eldar_h_asc2025.git
cd eldar_h_asc2025
2. Create a virtual environment (optional but recommended)

python -m venv venv
venv\Scripts\activate  # On Windows
3. Install dependencies

pip install -r requirements.txt
4. Create a .env file
Inside the root directory, create a .env file and add:

DISCORD_TOKEN=your_discord_bot_token
HF_API_KEY=
5. Run the bot

python run.py
📁 Project Structure

eldar_h_asc2025/
│
├── app/
│   ├── ai/
│   │   └── hf_ai.py          # Hugging Face API interface
│   ├── db/
│   │   └── database.py       # SQLite3 user tracking
│   └── quotes/
│       └── quotes.json       # Local fallback quotes
│
├── bot.py                    # Discord bot logic
├── run.py                    # Entrypoint
├── .env                      # API tokens (not included)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
🧪 Usage
/ai [style] [prompt] → Chat with AI in various styles

/cite [topic] → Get a quote about a topic

/lang az/en → Set your preferred response language

📜 Example Commands

/cite success
/lang az
/ai teacher What is a black hole?
🏁 Competition Requirement
This repository satisfies the competition deliverables:

✅ Fully functional AI Discord bot

✅ Hosted on GitHub

✅ Includes source code, documentation, and README

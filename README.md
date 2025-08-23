Discord Bot with Flask Keep-Alive (Railway Deployment)

This is a simple Discord bot built with discord.py that stays alive 24/7 using a Flask web server. Ideal for deployment on Railway
 using the free tier.

✅ Features

Discord bot using discord.py

Flask-based web server for health checks

Deployment on Railway for 24/7 uptime

📂 Project Structure
discord-bot/
├── bot.py              # Main bot script with Flask
├── requirements.txt    # Python dependencies
├── Procfile            # Defines the web process for Railway
└── README.md           # Documentation

🛠 Requirements

Python 3.10+

discord.py

Flask

A Discord Bot Token

🚀 Local Setup

Clone this repository

git clone https://github.com/your-username/discord-bot.git
cd discord-bot


Create a virtual environment

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Install dependencies

pip install -r requirements.txt


Set environment variable

export DISCORD_TOKEN=your-bot-token


Run the bot

python bot.py

🌐 Deploy on Railway (Free Hosting)
1. Prepare Files

Make sure your project has:

bot.py

requirements.txt

Procfile

2. Create Procfile

Add the following line:

web: python bot.py

3. Push to GitHub

Upload all files to your GitHub repo.

4. Deploy on Railway

Go to Railway
 and sign in.

Click New Project → Deploy from GitHub.

Select your repository.

Add an environment variable:

DISCORD_TOKEN = your-bot-token


Click Deploy.

✅ How It Works

Railway will run python bot.py as defined in Procfile.

Flask web server listens for pings to keep the container alive.

Discord bot runs in the same process.

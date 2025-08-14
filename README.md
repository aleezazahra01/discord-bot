# Kuromi Discord Bot 💬🎭

Kuromi  is a multipurpose Discord bot that can welcome new members with jokes, manage your server (ban, kick, mute, unmute), join/leave voice channels, and respond to fun commands.

---

## ✨ Features
- **Welcome New Members**  
  Greets new users in the welcome channel with a random joke from [JokeAPI](https://v2.jokeapi.dev/).

- **Fun Commands**
  - `=hello` → Says hello with a little attitude 😏
  - `=bye` → Says goodbye politely
  - `=joke` → Fetches a random joke on demand
  - `=ily` → Tells you it loves you back ❤️

- **Voice Channel Control**
  - `=join` → Joins your current voice channel
  - `=leave` → Leaves the voice channel

- **Moderation Tools**
  - `=ban @user [reason]` → Bans a member
  - `=kick @user [reason]` → Kicks a member
  - `=mute @user [time]` → Temporarily mutes a user (`10s`, `5m`, `1d`, `2w`)
  - `=unmute @user` → Removes mute

---

## 📦 Installation
pip install -r requirements.txt

3. Configure your bot token
Create a keys.py file and add:
bottoken = "YOUR_DISCORD_BOT_TOKEN"


5. Enable Intents in Discord Developer Portal
Go to your bot’s page in the Discord Developer Portal and enable the following,
Enable:
Message Content Intent
Server Members Intent

For all features to work, ensure the bot has:
1.Administrator (or appropriate moderation) permissions
2.Access to the welcome channel
3.Permission to connect & speak in voice channels

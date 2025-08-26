#  Discord Bot (24/7 Hosting with Flask + Railway)
A simple Discord bot using discord.py and Flask keep-alive server, deployed for free on Railway.
# Features:

✅ Discord bot using discord.py

✅ Flask web server for uptime

✅ Free hosting on Railway

✅ Easy to set up & deploy


## Project Structure
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
discord-bot/
├── bot.py             # Main bot file
├── requirements.txt   # Python dependencies
├── Procfile           # Railway start command
└── README.md          # Documentation

```

## Deploy on railway.app
1.Create Procfile
```bash
web: python bot.py
```
2.go to railway.app and deploy it from the repo.
3.declare the bottoken environmental variable with the bot token from discord for developers site.
4.then deploy it for free.

>>It crashed for like 50 times before getting deployed.



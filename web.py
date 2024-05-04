from flask import Flask
from threading import Thread
from app import RedditBot
from config import Config

app = Flask(__name__)
reddit_bot = RedditBot(Config.client_id, Config.client_secret, Config.username, Config.password)

@app.route('/')
def index():
    return 'Reddit Bot Web App'

@app.route('/start_bot')
def start_bot():
    thread = Thread(target=reddit_bot.run)
    thread.start()
    return 'Reddit Bot started successfully!'

@app.route('/stop_bot')
def stop_bot():
    if reddit_bot.is_running():
        reddit_bot.stop()
        return 'Reddit Bot stopped successfully!'
    else:
        return 'Reddit Bot is not running.'

@app.route('/log')
def log():
    with open("log.txt") as file:
        data = file.read()
        return data

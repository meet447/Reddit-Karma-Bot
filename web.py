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
    return 'Reddit Bot started successfully! checks the log at /log'

@app.route('/log')
def log():
    with open("log.txt") as file:
        data = file.read()
        return data
    
@app.route('/commented')
def commented_posts():
    with open("commented_posts.txt") as file:
        data = file.read()
        return data

from threading import Thread
from flask import Flask

app = Flask('')


@app.route('/')
def home():
    """Home page"""
    return "I'm alive"


def run():
    """App start function"""
    app.run(host='0.0.0.0', port=80)


def keep_alive():
    """Keep alive function"""
    t = Thread(target=run)
    t.start()

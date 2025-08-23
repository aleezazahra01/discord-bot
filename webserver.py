from flask import Flask 
from threading import Thread
app=Flask('')
app.route('/')
@app.route('/')
def home():
    return "discord bot ok"

def run():
    app.run(host='0.0.0.0', port=8080,debug=False)
def keep_alive():
    t = Thread(target=run)
    t.start()   



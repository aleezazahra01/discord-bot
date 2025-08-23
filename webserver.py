from flask import Flask 
from threading import Thread
app=Flask('')
app.route('/')
@app.route('/')
def home():
    return "discord bot ok"

def run():
    port = int(os.environ.get("PORT", 8080))  # Railway requires PORT env
    app.run(host="0.0.0.0", port=port)
def keep_alive():
    t = Thread(target=run)
    t.start()   


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False, threaded=False)



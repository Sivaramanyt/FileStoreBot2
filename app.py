import os, asyncio, requests
from flask import Flask, request, abort, jsonify
from telegram import Update
from bot import build_app  # build Application without running a loop
from config import WEBHOOK_SECRET, BASE_URL, BOT_TOKEN, PREMIUM_QR_URL

app = Flask(__name__)

# Build the PTB Application once at import time (Flask 3.x compatible)
application = build_app()

def fetch_qr():
    os.makedirs("static", exist_ok=True)
    try:
        r = requests.get(PREMIUM_QR_URL, timeout=10)
        with open("static/upi_qr.jpg", "wb") as f:
            f.write(r.content)
    except:
        pass

# Run any one-time setup here (no before_first_request in Flask 3)
fetch_qr()

@app.get("/")
def index():
    return "File Store Bot is running."

@app.post(f"/webhook/{WEBHOOK_SECRET}")
def webhook():
    if not request.headers.get("Content-Type", "").startswith("application/json"):
        abort(415)
    update = Update.de_json(request.get_json(force=True), application.bot)
    # Process the update in an isolated event loop for this request
    asyncio.run(application.process_update(update))
    return jsonify(ok=True)

@app.get("/setup")
def setup():
    url = f"{BASE_URL}/webhook/{WEBHOOK_SECRET}"
    r = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook", data={"url": url})
    return r.text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
    

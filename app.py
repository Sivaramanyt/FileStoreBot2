import os, asyncio, requests
from flask import Flask, request, abort, jsonify
from telegram import Update
from bot import init_application, application
from config import WEBHOOK_SECRET, BASE_URL, BOT_TOKEN, PREMIUM_QR_URL

app = Flask(__name__)

@app.before_first_request
def setup_runtime():
    # Initialize PTB Application and fetch QR once at startup
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_application())
    fetch_qr()

@app.get("/")
def index():
    return "File Store Bot is running."

@app.post(f"/webhook/{WEBHOOK_SECRET}")
def webhook():
    if request.headers.get("Content-Type") != "application/json":
        abort(415)
    update = Update.de_json(request.get_json(force=True), application.bot)
    # Process the update synchronously in this request
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.process_update(update))
    return jsonify(ok=True)

@app.get("/setup")
def setup():
    url = f"{BASE_URL}/webhook/{WEBHOOK_SECRET}"
    r = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook", data={"url": url})
    return r.text

def fetch_qr():
    os.makedirs("static", exist_ok=True)
    try:
        r = requests.get(PREMIUM_QR_URL, timeout=15)
        with open("static/upi_qr.jpg", "wb") as f:
            f.write(r.content)
    except:
        pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))

import os, json

BOT_TOKEN = os.getenv("BOT_TOKEN", "8219734500:AAG3hD8fPirprlr4OZEYF4oLr09UVWr_e9s")
BASE_URL = os.getenv("BASE_URL", "https://faint-allegra-rolexsir-7a1ec4b1.koyeb.app")  # e.g. https://yourapp-org.koyeb.app
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://Sivaraman444:Rama9789@cluster0.8lxln.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.getenv("DB_NAME", "cluster0")

OWNER_ID = int(os.getenv("OWNER_ID", "1206988513") or 0)
ADMINS = [int(x) for x in os.getenv("ADMINS", "").split() if x.strip().isdigit()]

FORCE_SUB_CHANNELS = [int(x) for x in os.getenv("FORCE_SUB_CHANNELS", "-1002429072244").split(",") if x.strip().startswith("-100")]
FREE_VIDEO_LIMIT = int(os.getenv("FREE_VIDEO_LIMIT", "3"))

SHORTLINK_PROVIDERS = json.loads(os.getenv("SHORTLINK_PROVIDERS", "[]"))
VERIFY_EXPIRE = int(os.getenv("VERIFY_EXPIRE", "86400"))

PREMIUM_UPI_ID = os.getenv("PREMIUM_UPI_ID", "sivaramanc49@okaxis")
PREMIUM_QR_URL = os.getenv("PREMIUM_QR_URL", "https://envs.sh/in5.jpg")

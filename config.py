import os, json

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BASE_URL = os.getenv("BASE_URL", "")  # e.g. https://yourapp-org.koyeb.app
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

MONGO_URL = os.getenv("MONGO_URL", "")
DB_NAME = os.getenv("DB_NAME", "filestorebot")

OWNER_ID = int(os.getenv("OWNER_ID", "0") or 0)
ADMINS = [int(x) for x in os.getenv("ADMINS", "").split() if x.strip().isdigit()]

FORCE_SUB_CHANNELS = [int(x) for x in os.getenv("FORCE_SUB_CHANNELS", "").split(",") if x.strip().startswith("-100")]
FREE_VIDEO_LIMIT = int(os.getenv("FREE_VIDEO_LIMIT", "3"))

SHORTLINK_PROVIDERS = json.loads(os.getenv("SHORTLINK_PROVIDERS", "[]"))
VERIFY_EXPIRE = int(os.getenv("VERIFY_EXPIRE", "86400"))

PREMIUM_UPI_ID = os.getenv("PREMIUM_UPI_ID", "sivaramanc49@okaxis")
PREMIUM_QR_URL = os.getenv("PREMIUM_QR_URL", "https://envs.sh/in5.jpg")

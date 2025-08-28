from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import BOT_TOKEN
from handlers.start import start
from handlers.upload import handle_document, handle_video
from handlers.retrieve import get_cmd
from handlers.verify import verify_callback
from handlers.admin import resetverify_cmd, users_cmd, broadcast_cmd
from payments import premium_cmd, setpremium_cmd

def build_app() -> Application:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get", get_cmd))
    app.add_handler(CommandHandler("resetverify", resetverify_cmd))
    app.add_handler(CommandHandler("users", users_cmd))
    app.add_handler(CommandHandler("broadcast", broadcast_cmd))
    app.add_handler(CommandHandler("premium", premium_cmd))
    app.add_handler(CommandHandler("setpremium", setpremium_cmd))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(CallbackQueryHandler(verify_callback, pattern=r"^vchk:"))
    return app

application = None

async def init_application():
    global application
    application = build_app()
    await application.initialize()

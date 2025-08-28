from telegram import Update
from telegram.ext import ContextTypes
from db import ensure_user, bump_stat
from handlers.retrieve import deliver_code

WELCOME = (
    "Welcome to the File Store Bot.\n"
    "• Send files or videos to get a permanent deep link.\n"
    "• First 3 videos are free; after that, complete verification or go premium.\n"
    "Commands: /premium, /get <code>, /users (admin), /broadcast (admin reply), /resetverify <user_id> (admin)."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ensure_user(update.effective_user.id)
    bump_stat("starts", 1)
    # handle deep-links like dl_<code> and vt_<signed>_<code>
    args = context.args
    if args:
        arg = args
        if arg.startswith("dl_"):
            code = arg[3:]
            await deliver_code(update, context, code)
            return
        elif arg.startswith("vt_"):
            # Click-through; actual verification completion via button press
            await update.message.reply_text("Return to the chat and click 'I Verified' to get your file.")
            return
    await update.message.reply_text(WELCOME)

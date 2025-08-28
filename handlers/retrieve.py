from telegram import Update
from telegram.ext import ContextTypes
from db import get_file_by_code, increment_free_used
from utils import reached_free_limit
from handlers.verify import start_verification_flow

async def deliver_code(update: Update, context: ContextTypes.DEFAULT_TYPE, code: str):
    f = get_file_by_code(code)
    if not f:
        await update.effective_message.reply_text("Invalid or missing code.")
        return
    uid = update.effective_user.id
    if f["type"] == "video" and reached_free_limit(uid):
        await start_verification_flow(update, context, target_code=code)
        return
    if f["type"] == "video":
        increment_free_used(uid)
    await update.effective_message.reply_text("Sending...")
    if f["type"] == "video":
        await update.effective_message.reply_video(video=f["tg_file_id"], caption=f.get("caption", ""))
    else:
        await update.effective_message.reply_document(document=f["tg_file_id"], caption=f.get("caption", ""))

async def get_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parts = (update.message.text.split() if update.message else [])
    if len(parts) < 2:
        await update.message.reply_text("Usage: /get <code>")
        return
    code = parts[1].strip()
    await deliver_code(update, context, code)

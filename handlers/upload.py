from telegram import Update
from telegram.ext import ContextTypes
from db import create_file
from handlers.subscribe import ensure_subscribed

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_subscribed(update, context): return
    doc = update.message.document
    code = create_file(update.effective_user.id, doc.file_id, "document", doc.file_name or "", doc.file_size or 0)
    me = await context.bot.get_me()
    link = f"https://t.me/{me.username}?start=dl_{code}"
    await update.message.reply_text(f"Permanent link:\n{link}")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_subscribed(update, context): return
    vid = update.message.video
    code = create_file(update.effective_user.id, vid.file_id, "video", "", vid.file_size or 0)
    me = await context.bot.get_me()
    link = f"https://t.me/{me.username}?start=dl_{code}"
    await update.message.reply_text(f"Permanent link:\n{link}")

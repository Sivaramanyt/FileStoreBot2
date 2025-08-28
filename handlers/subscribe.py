from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from config import FORCE_SUB_CHANNELS

def force_sub_kb():
    buttons = [[InlineKeyboardButton("Join Channel", url=f"https://t.me/c/{str(ch)[4:]}")] for ch in FORCE_SUB_CHANNELS]
    return InlineKeyboardMarkup(buttons)

async def ensure_subscribed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if not FORCE_SUB_CHANNELS:
        return True
    from utils import check_force_sub
    ok = await check_force_sub(update, context)
    if not ok:
        await update.effective_message.reply_text("Please join the required channel(s) to continue.", reply_markup=force_sub_kb())
    return ok

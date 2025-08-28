from telegram import Update
from telegram.ext import ContextTypes
from db import set_premium
from config import PREMIUM_UPI_ID
from handlers.admin import is_admin

async def premium_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"Premium unlock via UPI/GPay.\n"
        f"UPI ID: {PREMIUM_UPI_ID}\n"
        f"Pay and send the screenshot to the admin.\n"
        f"Admins will activate premium. Or continue with ad verification after the free limit."
    )
    try:
        with open("static/upi_qr.jpg", "rb") as f:
            await update.message.reply_photo(photo=f, caption=text)
    except:
        await update.message.reply_text(text)

async def setpremium_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /setpremium <user_id> <on|off>")
        return
    uid = int(context.args); val = context.args[1].lower() == "on"
    set_premium(uid, val)
    await update.message.reply_text(f"Premium {'enabled' if val else 'disabled'} for {uid}.")

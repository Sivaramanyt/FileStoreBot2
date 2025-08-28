from telegram import Update
from telegram.ext import ContextTypes
from db import reset_verification, count_users, broadcasts, users
from config import OWNER_ID, ADMINS

def is_admin(uid: int) -> bool:
    return uid == OWNER_ID or uid in ADMINS

async def resetverify_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /resetverify <user_id>")
        return
    uid = int(context.args)
    reset_verification(uid)
    await update.message.reply_text(f"Verification reset for {uid}.")

async def users_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    await update.message.reply_text(f"Total users: {count_users()}")

async def broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a message with /broadcast to send it to all users.")
        return
    cur = users.find({}, {"_id": 1})
    total = 0; ok = 0; fail = 0
    for doc in cur:
        total += 1
        try:
            await update.message.reply_to_message.copy(chat_id=doc["_id"])
            ok += 1
        except:
            fail += 1
    broadcasts.insert_one({"total": total, "success": ok, "failed": fail})
    await update.message.reply_text(f"Broadcast done. Success {ok}/{total}.")

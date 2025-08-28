from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from itsdangerous import TimestampSigner, BadSignature
from db import get_active_verification, create_verification, mark_verified, get_file_by_code
from shortlink import shorten_once
from utils import gen_token

signer = TimestampSigner("verify-secret")  # you can derive from WEBHOOK_SECRET if desired

async def start_verification_flow(update: Update, context: ContextTypes.DEFAULT_TYPE, target_code: str):
    uid = update.effective_user.id
    active = get_active_verification(uid)
    if active:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("Verification Link", url=active["short_url"])]])
        await update.effective_message.reply_text("Complete verification, then click 'I Verified'.", reply_markup=kb)
        return
    raw_token = gen_token()
    signed = signer.sign(raw_token).decode()
    me = await context.bot.get_me()
    verify_deeplink = f"https://t.me/{me.username}?start=vt_{signed}_{target_code}"
    try:
        provider, short_url = shorten_once(verify_deeplink)
    except Exception:
        short_url = verify_deeplink
        provider = "direct"
    create_verification(uid, provider, short_url, signed)
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("Verification Link", url=short_url)],
        [InlineKeyboardButton("I Verified", callback_data=f"vchk:{signed}:{target_code}")]
    ])
    await update.effective_message.reply_text("Please open the verification link, wait, then return and press 'I Verified'.", reply_markup=kb)

async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    _, signed, code = q.data.split(":", 2)
    try:
        signer.unsign(signed, max_age=86400)
    except BadSignature:
        await q.message.edit_text("Verification expired. Use the link again.")
        return
    mark_verified(signed)
    f = get_file_by_code(code)
    if not f:
        await q.message.edit_text("Target file not found. Try /get again.")
        return
    await q.message.edit_text("Verified! Delivering your file...")
    if f["type"] == "video":
        await q.message.reply_video(video=f["tg_file_id"], caption=f.get("caption", ""))
    else:
        await q.message.reply_document(document=f["tg_file_id"], caption=f.get("caption", ""))

import secrets
from telegram import Update
from telegram.constants import ChatMemberStatus
from telegram.ext import ContextTypes
from config import FORCE_SUB_CHANNELS, FREE_VIDEO_LIMIT
from db import ensure_user, is_premium

def gen_token() -> str:
    return secrets.token_urlsafe(16)

async def check_force_sub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if not FORCE_SUB_CHANNELS:
        return True
    user_id = update.effective_user.id
    for ch in FORCE_SUB_CHANNELS:
        try:
            m = await context.bot.get_chat_member(chat_id=ch, user_id=user_id)
            if m.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                return False
        except:
            return False
    return True

def reached_free_limit(user_id: int) -> bool:
    u = ensure_user(user_id)
    if is_premium(user_id):
        return False
    return u.get("free_used", 0) >= FREE_VIDEO_LIMIT

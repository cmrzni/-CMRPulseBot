from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import json, os

TOKEN = os.getenv("8848112088:AAFrQFJnjcFKESHCkuL35dih5Zn4n596ZwA")
ADMIN_ID = 8551328912  # آیدی عددی خودت

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_chat.id
    users = load_users()
    if uid not in users:
        users.append(uid)
        save_users(users)
    await update.message.reply_text("عضویت ثبت شد. سیگنال‌ها برایت ارسال می‌شود.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text(f"Users: {len(load_users())}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    users = load_users()

    for uid in users:
        try:
            await context.bot.copy_message(
                chat_id=uid,
                from_chat_id=update.effective_chat.id,
                message_id=update.message.message_id
            )
        except:
            pass

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))

# هر پیامی که ادمین به ربات بفرستد برای همه ارسال می‌شود
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, broadcast))

app.run_polling()

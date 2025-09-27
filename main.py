import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ডিফল্ট সেটিংস (তোমার টোকেন, API URL, ইত্যাদি এখানে বসানো)
TG_TOKEN = "8341027913:AAFOh6mr3VNrD2XMOFRrYqes_c0wmQZ86CI"
API_BASE = "https://flamelk-likes.onrender.com"
ADMIN_ID = 5545907758
REGION_DEFAULT = "ME"
DAILY_LIMIT = 100

user_daily_count = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"হ্যালো {update.effective_user.first_name}!\n"
        f"প্রতিদিন সর্বোচ্চ {DAILY_LIMIT} লাইক নিতে পারবেন।\n"
        f"UID দিয়ে /like কমান্ড ব্যবহার করুন।\n"
        f"যেমন: /like 123456789"
    )

async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if len(context.args) != 1:
        await update.message.reply_text("❗ সঠিক ব্যবহার: /like <UID>")
        return

    uid = context.args[0]
    count = user_daily_count.get(user_id, 0)

    if count >= DAILY_LIMIT:
        await update.message.reply_text("⚠️ আজকের জন্য লাইক লিমিট শেষ। আবার কাল চেষ্টা করুন।")
        return

    headers = {
        "authorization": "Bearer dummy_token",  # যদি প্রয়োজন হয় এখানে সঠিক টোকেন বসাও
        "Content-Type": "application/json"
    }
    payload = {
        "region": REGION_DEFAULT,
        "uid": uid,
        "payload": ""  # প্রয়োজন হলে এখানে ডাটা দিবে
    }

    try:
        response = requests.post(f"{API_BASE}/send-likes", json=payload, headers=headers)
        data = response.json()

        if response.status_code == 200 and data.get("message") != "Invalid or expired session":
            user_daily_count[user_id] = count + 1
            await update.message.reply_text(f"✅ UID: {uid} এর জন্য লাইক পাঠানো হয়েছে! (আজকের লাইক: {user_daily_count[user_id]})")
        else:
            await update.message.reply_text(f"❌ লাইক পাঠানো যায়নি: {data.get('message', 'Unknown error')}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ এরর: {e}")

def main():
    app = ApplicationBuilder().token(TG_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("like", like))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

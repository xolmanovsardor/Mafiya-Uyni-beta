import os
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from game import assign_roles, vote, end_day, check_winner, load_data, save_data

# .env dan tokenni olish
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# O'yin holati (kutish ro'yxati) - ma'lumotlar endi faylda saqlanadi


# /join — o‘yinga qo‘shilish
async def join_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id = str(update.message.from_user.id)
    
    if user_id in data.get("waiting", []):
        await update.message.reply_text("⚠️ Siz allaqachon o‘yindasiz.")
        return
    
    data["waiting"].append(user_id)
    # Foydalanuvchi haqida ma'lumotni ham saqlaymiz
    if "players_info" not in data:
        data["players_info"] = {}
    
    user = update.message.from_user
    data["players_info"][user_id] = {
        "username": user.username or "",
        "name": user.full_name or ""
    }
    
    save_data(data)
    await update.message.reply_text("✅ Siz o‘yinga qo‘shildingiz.")


# /startgame — o‘yinni boshlash
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    waiting = data.get("waiting", [])
    
    if len(waiting) < 2:
        await update.message.reply_text("⚠️ O‘yin boshlash uchun kamida 2 ta o‘yinchi kerak.")
        return

    assigned = assign_roles(waiting)
    data["players"] = assigned  # Rollar haqida ma'lumotni saqlaymiz
    
    for player, info in assigned.items():
        try:
            await context.bot.send_message(
                chat_id=int(player),  # player ni butun songa o'tkazamiz
                text=f"🎭 Sizning rolingiz: {info['role']}"
            )
        except Exception as e:
            print(f"{player} ga xabar yuborishda xatolik: {e}")
            await update.message.reply_text(f"⚠️ {player} ga xabar yuborib bo‘lmadi.")

    # Kutish ro'yxatini tozalaymiz va ma'lumotlarni saqlaymiz
    data["waiting"] = []
    save_data(data)
    
    await update.message.reply_text("🎯 O‘yin boshlandi! Rollar tarqatildi.")


# /vote — ovoz berish
async def vote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("ℹ️ Foydalanish: /vote <player_id>")
        return

    voter = str(update.message.from_user.id)
    target = context.args[0]
    success, msg = vote(voter, target)
    await update.message.reply_text(msg)


# /endday — kunni yakunlash
async def end_day_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    executed, msg = end_day()
    await update.message.reply_text(msg)

    winner, win_msg = check_winner()
    if winner:
        await update.message.reply_text(f"🏆 {win_msg}")


# /status — hozirgi holatni ko‘rsatish
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    waiting = data.get("waiting", [])
    players_info = data.get("players_info", {})

    text = "⏺️ Kutish ro'yxati:\n"
    if not waiting:
        text += " - Hech kim yo‘q\n"
    else:
        for uid in waiting:
            info = players_info.get(uid, {})
            name = info.get("name", "?")
            username = info.get("username", "")
            if username:
                username = f"@{username}"
            text += f" - {name} {username} — id: {uid}\n"

    await update.message.reply_text(text)


# Asosiy ishga tushirish
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("join", join_game))
    app.add_handler(CommandHandler("startgame", start_game))
    app.add_handler(CommandHandler("vote", vote_command))
    app.add_handler(CommandHandler("endday", end_day_command))
    app.add_handler(CommandHandler("status", status_command))

    app.run_polling()


if name == "main":
    main()
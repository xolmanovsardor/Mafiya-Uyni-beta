import json
import os

DATA_FILE = "data.json"

# Faylni yaratish yoki o'qish
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"waiting": [], "players_info": {}, "roles": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Faylga yozish
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Kutish ro'yxatiga o'yinchi qo'shish
def add_player(user_id, name, username):
    data = load_data()
    if user_id not in data["waiting"]:
        data["waiting"].append(user_id)
        data["players_info"][user_id] = {
            "name": name,
            "username": username or ""
        }
        save_data(data)
        return True
    return False

# Rollarni taqsimlash (soddalashtirilgan)
import random
ROLES = ["Mafia", "Sherif", "Oddiy fuqaro"]

def assign_roles(players):
    data = load_data()
    roles = {}
    for player in players:
        role = random.choice(ROLES)
        roles[player] = {"role": role}
        data["roles"][player] = role
    save_data(data)
    return roles

# Ovoz berish (hozircha faqat oddiy)
votes = {}

def vote(voter, target):
    votes[voter] = target
    return True, f"✅ Siz {target} ga ovoz berdingiz."

# Kun yakuni
def end_day():
    if not votes:
        return None, "⚠️ Hech kimga ovoz berilmadi."
    # Eng ko'p ovoz olgan odamni topish
    from collections import Counter
    most_voted = Counter(votes.values()).most_common(1)[0][0]
    return most_voted, f"❌ {most_voted} o‘yinchi o‘yindan chiqarildi."

# G'olibni tekshirish (soddalashtirilgan)
def check_winner():
    return None, "O‘yin davom etmoqda."

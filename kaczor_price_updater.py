# kaczor_price_updater.py
# Wersja FINAL – tylko powiadomienia o spadkach cen + auto-update strony

import requests
import re
from datetime import datetime

# TWOJA BAZA GIER (1:1 z HTML)
games_database = [
    {"title": "Mafia II: Definitive Edition", "file": "Mafia_II_Definitive_Edition", "price": 23},
    {"title": "Batman: Arkham Asylum (GOTY)", "file": "Batman_Arkham_Asylum_GOTY", "price": 10},
    {"title": "Batman: Arkham City (GOTY)", "file": "Batman_Arkham_City_GOTY", "price": 10},
    {"title": "Batman: Arkham Collection", "file": "Batman_Arkham_Collection", "price": 24},
    {"title": "Batman: Arkham Knight (Premium)", "file": "Batman_Arkham_Knight_Premium", "price": 15},
    {"title": "Mafia III: Definitive Edition", "file": "Mafia_III_Definitive_Edition", "price": 25},
    {"title": "Mafia: Trilogy", "file": "Mafia_Trilogy", "price": 36},
    {"title": "Sid Meier's Civilization VI", "file": "Sid_Meiers_Civilization_VI", "price": 13},
    {"title": "Batman: Arkham Origins", "file": "Batman_Arkham_Origins", "price": 15},
    {"title": "Fallout 76", "file": "Fallout_76", "price": 42},
    {"title": "Ghost of Tsushima | Director's Cut", "file": "Ghost_of_Tsushima_Directors_Cut", "price": 117},
    {"title": "Ready or Not", "file": "Ready_or_Not", "price": 98},
    {"title": "Hogwarts Legacy | Deluxe Edition", "file": "Hogwarts_Legacy_Deluxe_Edition", "price": 50},
    {"title": "Mortal Kombat XL", "file": "Mortal_Kombat_XL", "price": 15},
    {"title": "Hello Neighbor", "file": "Hello_Neighbor", "price": 20},
    {"title": "Dying Light | Essentials Edition", "file": "Dying_Light_Essentials_Edition", "price": 20},
    {"title": "Marvel's Spider-Man Remastered", "file": "Marvels_Spider_Man_Remastered", "price": 81},
    {"title": "Hello Neighbor 2", "file": "Hello_Neighbor_2", "price": 21},
    {"title": "Subnautica", "file": "Subnautica", "price": 57},
    {"title": "Mortal Kombat 1", "file": "Mortal_Kombat_1", "price": 40},
    {"title": "Hitman: Absolution", "file": "Hitman_Absolution", "price": 10},
    {"title": "Hitman: World of Assassination", "file": "Hitman_World_of_Assassination", "price": 90},
    {"title": "Red Dead Redemption 2", "file": "Red_Dead_Redemption_2", "price": 55, "platform": "rockstar"},
    {"title": "Grand Theft Auto V (GTA V)", "file": "GTA_V", "price": 48, "platform": "rockstar"},
    {"title": "Days Gone", "file": "Days_Gone", "price": 69},
    {"title": "DOOM (2016)", "file": "DOOM", "price": 20},
    {"title": "TEKKEN 7", "file": "Tekken_7", "price": 30},
    {"title": "TEKKEN 8", "file": "Tekken_8", "price": 92},
    {"title": "Back 4 Blood", "file": "Back_4_Blood", "price": 14},
    {"title": "Hellblade: Senua's Sacrifice", "file": "Hellblade_Senuas_Sacrifice", "price": 25},
    {"title": "Metro Exodus Gold Edition", "file": "Metro_Exodus_Gold", "price": 28},
    {"title": "Terraria", "file": "Terraria", "price": 34},
    {"title": "Hearts of Iron IV", "file": "Hearts_of_Iron_IV", "price": 44},
    {"title": "Hunt: Showdown", "file": "Hunt_Showdown", "price": 62},
    {"title": "God of War (2022)", "file": "God_of_War", "price": 69},
    {"title": "Marvel's Spider-Man: Miles Morales", "file": "SpiderMan_Miles_Morales", "price": 69},
    {"title": "S.T.A.L.K.E.R. 2: Heart of Chornobyl", "file": "Stalker_2", "price": 127},
    {"title": "Horizon Forbidden West Complete Edition", "file": "Horizon_Forbidden_West_Complete", "price": 128},
    {"title": "Amanda the Adventurer", "file": "Amanda_The_Adventurer", "price": 10},
    {"title": "Bendy and the Ink Machine", "file": "Bendy_And_The_Ink_Machine", "price": 10},
    {"title": "LEGO Batman Trilogy", "file": "LEGO_Batman_Trilogy", "price": 20},
    {"title": "Carrion", "file": "Carrion", "price": 21},
    {"title": "Predator: Hunting Grounds", "file": "Predator_Hunting_Grounds", "price": 35}
]

MY_PROFIT = 5
HTML_FILE = "index.html"
LOG_FILE = "price_log.txt"

# TWÓJ DISCORD WEBHOOK
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1444394230104592557/yrk7HO10APUmMSuC6jHRPgsmVmQ05I8Z7ff9N2c3xTsgA5R3h-kEyPXXBgnV-lb3kxVq"

def send_to_discord(msg):
    try:
        requests.post(DISCORD_WEBHOOK, json={"content": msg})
    except:
        pass

# Instant-Gaming – tylko czyste klucze Steam EU/Global
def get_instant_price(title):
    try:
        q = title.split("|")[0].strip().replace(" ", "+")
        url = f"https://www.instant-gaming.com/en/search/?query={q}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
        if any(bad in r.text.lower() for bad in ["account", "gift", "russia", "turkey", "argentina"]):
            return None, None
        m = re.search(r'data-price="([\d,.]+)"', r.text)
        if m:
            eur = float(m.group(1).replace(",", "."))
            return round(eur * 4.31, 2), url
    except:
        pass
    return None, None

# G2A – tylko czyste klucze Steam EU/Global
def get_g2a_price(title):
    try:
        q = title.split("|")[0].strip().replace(" ", "+")
        url = f"https://www.g2a.com/search?query={q}&currency=PLN&country=PL"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
        if any(bad in r.text.lower() for bad in ["account", "gift", "russia", "turkey", "argentina", "cis", "latam"]):
            return None, None
        if "steam" not in r.text.lower():
            return None, None
        m = re.search(r'"price":\s*([\d.]+)', r.text)
        if m:
            return round(float(m.group(1)), 2), url
    except:
        pass
    return None, None

# === GŁÓWNE DZIAŁANIE ===
changes = []

for game in games_database:
    title = game["title"]
    old_price = game["price"]

    ig_price, ig_link = get_instant_price(title)
    g2a_price, g2a_link = get_g2a_price(title)

    offers = []
    if ig_price: offers.append((ig_price, ig_link, "Instant"))
    if g2a_price: offers.append((g2a_price, g2a_link, "G2A"))

    if not offers:
        continue

    best_price, link, shop = min(offers, key=lambda x: x[0])
    new_price = round(best_price + MY_PROFIT)

    if new_price < old_price or abs(new_price - old_price) >= 3:
        game["price"] = new_price
        changes.append(f"**{title[:50]}** `{old_price}zł → {new_price}zł` | {shop}")

# === ZAPIS DO HTML + DISCORD TYLKO GDY SĄ ZMIANY ===
if changes:
    # Aktualizacja index.html
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    new_js_block = "const gamesDatabase = [\n"
    for g in games_database:
        plat = ',platform:"rockstar"' if g.get("platform") == "rockstar" else ""
        new_js_block += f'    {{file:"{g["file"]}",title:"{g["title"]}",price:{g["price"]}{plat}}},\n'
    new_js_block += "];"

    content = re.sub(r'const gamesDatabase\s*=\s*\[.*?\];', new_js_block, content, flags=re.DOTALL)

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    # Log do pliku
    with open(LOG_FILE, "a", encoding="utf-8") as logf:
        logf.write(f"\n=== {datetime.now().strftime('%d.%m.%Y %H:%M')} ===\n")
        for line in changes:
            logf.write(line.replace("**", "").replace("`", "") + "\n")

    # Powiadomienie na Discorda
    discord_msg = "**KWAK! Ceny spadły!**\n\n" + "\n".join(changes) + \
                  f"\n\nPełny log: https://github.com/TWÓJ_LOGIN/TWOJE_REPO/blob/main/price_log.txt"
    send_to_discord(discord_msg)

    print(f"Wysłano {len(changes)} zmian na Discorda!")
else:
    print("Zero zmian cenowych – brak powiadomienia")

print("KWAK KWAK – updater skończony")

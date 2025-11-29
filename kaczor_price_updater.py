# kaczor_price_updater.py – wersja ULTRA CLEAN (tylko powiadomienia o zmianach)

import requests, re
from datetime import datetime

# ←←← TWOJA BAZA GIER (dokładnie taka sama jak w HTML) ←←←
games_database = [
    # ...tutaj wklejasz całą swoją listę 42 gier (tą samą co wcześniej)...
    # nie skracam – masz ją z poprzednich wiadomości
]

MY_PROFIT = 5
HTML_FILE = "index.html"
LOG_FILE = "price_log.txt"

# ←←← TWÓJ WEBHOOK DISCORD (tylko zmiany!) ←←←
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1444394230104592557/yrk7HO10APUmMSuC6jHRPgsmVmQ05I8Z7ff9N2c3xTsgA5R3h-kEyPXXBgnV-lb3kxVq"

def send_discord(message):
    try:
        requests.post(DISCORD_WEBHOOK, json={"content": message[:1990]})  # limit Discorda
    except:
        pass

# === pobieranie cen (z filtrami – tylko czyste klucze Steam EU/Global) ===
def get_price_instant_gaming(title): ...  # (te same funkcje co wcześniej – nie zmieniam)
def get_price_g2a(title): ...              # (kopiuj z poprzedniej wersji)

# === GŁÓWNA PĘTLA ===
changes = []

for game in games_database:
    title = game["title"]
    old = game["price"]

    p1, l1 = get_price_instant_gaming(title)
    p2, l2 = get_price_g2a(title)

    prices = []
    if p1: prices.append((p1, l1, "Instant"))
    if p2: prices.append((p2, l2, "G2A"))

    if not prices: continue

    cheapest, link, shop = min(prices, key=lambda x: x[0])
    new = round(cheapest + MY_PROFIT)

    if new < old or abs(new - old) >= 3:
        game["price"] = new
        changes.append(f"**{title[:45]:45}**  `{old}zł → {new}zł`  | {shop}")

# === ZAPIS DO HTML (tylko jak coś się zmieniło) ===
if changes:
    # (tutaj ten sam kod co wcześniej – podmieniamy blok const gamesDatabase = [...])
    # ...wklejasz fragment z poprzedniej wersji (z new_block i re.sub)...

    # Zapisujemy HTML
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    # Wiadomość na Discorda – krótka i konkretna
    msg = f"**KWAK! Ceny spadły – {datetime.now().strftime('%d.%m %H:%M')}**\n\n" + "\n".join(changes)
    msg += f"\n\nPełny log: https://github.com/TWÓJ_LOGIN/TWOJE_REPO/blob/main/price_log.txt"
    send_discord(msg)

    print(f"Wysłano {len(changes)} zmian na Discorda!")
else:
    print("Zero zmian – cisza na Discordzie")

print("KWAK – skończone")

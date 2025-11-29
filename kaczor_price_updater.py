# kaczor_price_updater.py – wersja ULTRA CLEAN (tylko powiadomienia o zmianach)

import requests, re
from datetime import datetime

# ←←← TWOJA BAZA GIER (dokładnie taka sama jak w HTML) ←←←
games_database = [
  {file:"Mafia_II_Definitive_Edition",title:"Mafia II: Definitive Edition",price:23},
    {file:"Batman_Arkham_Asylum_GOTY",title:"Batman: Arkham Asylum (GOTY)",price:10},
    {file:"Batman_Arkham_City_GOTY",title:"Batman: Arkham City (GOTY)",price:10},
    {file:"Batman_Arkham_Collection",title:"Batman: Arkham Collection",price:24},
    {file:"Batman_Arkham_Knight_Premium",title:"Batman: Arkham Knight (Premium)",price:15},
    {file:"Mafia_III_Definitive_Edition",title:"Mafia III: Definitive Edition",price:25},
    {file:"Mafia_Trilogy",title:"Mafia: Trilogy",price:36},
    {file:"Sid_Meiers_Civilization_VI",title:"Sid Meier's Civilization VI",price:13},
    {file:"Batman_Arkham_Origins",title:"Batman: Arkham Origins",price:15},
    {file:"Fallout_76",title:"Fallout 76",price:42},
    {file:"Ghost_of_Tsushima_Directors_Cut",title:"Ghost of Tsushima | Director's Cut",price:117},
    {file:"Ready_or_Not",title:"Ready or Not",price:98},
    {file:"Hogwarts_Legacy_Deluxe_Edition",title:"Hogwarts Legacy | Deluxe Edition",price:50},
    {file:"Mortal_Kombat_XL",title:"Mortal Kombat XL",price:15},
    {file:"Hello_Neighbor",title:"Hello Neighbor",price:20},
    {file:"Dying_Light_Essentials_Edition",title:"Dying Light | Essentials Edition",price:20},
    {file:"Marvels_Spider_Man_Remastered",title:"Marvel's Spider-Man Remastered",price:81},
    {file:"Hello_Neighbor_2",title:"Hello Neighbor 2",price:21},
    {file:"Subnautica",title:"Subnautica",price:57},
    {file:"Mortal_Kombat_1",title:"Mortal Kombat 1",price:40},
    {file:"Hitman_Absolution",title:"Hitman: Absolution",price:10},
    {file:"Hitman_World_of_Assassination",title:"Hitman: World of Assassination",price:90},
    {file:"Red_Dead_Redemption_2",title:"Red Dead Redemption 2",price:55,platform:"rockstar"},
    {file:"GTA_V",title:"Grand Theft Auto V (GTA V)",price:48,platform:"rockstar"},
    {file:"Days_Gone",title:"Days Gone",price:69},
    {file:"DOOM",title:"DOOM (2016)",price:20},
    {file:"Tekken_7",title:"TEKKEN 7",price:30},
    {file:"Tekken_8",title:"TEKKEN 8",price:92},
    {file:"Back_4_Blood",title:"Back 4 Blood",price:14},
    {file:"Hellblade_Senuas_Sacrifice",title:"Hellblade: Senua's Sacrifice",price:25},
    {file:"Metro_Exodus_Gold",title:"Metro Exodus Gold Edition",price:28},
    {file:"Terraria",title:"Terraria",price:34},
    {file:"Hearts_of_Iron_IV",title:"Hearts of Iron IV",price:44},
    {file:"Hunt_Showdown",title:"Hunt: Showdown",price:62},
    {file:"God_of_War",title:"God of War (2022)",price:69},
    {file:"SpiderMan_Miles_Morales",title:"Marvel's Spider-Man: Miles Morales",price:69},
    {file:"Stalker_2",title:"S.T.A.L.K.E.R. 2: Heart of Chornobyl",price:127},
    {file:"Horizon_Forbidden_West_Complete",title:"Horizon Forbidden West Complete Edition",price:128},
    {file:"Amanda_The_Adventurer",title:"Amanda the Adventurer",price:10},
    {file:"Bendy_And_The_Ink_Machine",title:"Bendy and the Ink Machine",price:10},
    {file:"LEGO_Batman_Trilogy",title:"LEGO Batman Trilogy",price:20},
    {file:"Carrion",title:"Carrion",price:21},
    {file:"Predator_Hunting_Grounds",title:"Predator: Hunting Grounds",price:35}
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

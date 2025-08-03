import math
import os
from dotenv import load_dotenv
from interactions import (
    Client, CommandContext, Intents, OptionType,
    slash_command, SlashCommandOption
)

# Wczytanie .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Konfiguracja klienta
bot = Client(token=TOKEN, intents=Intents.DEFAULT)

# 🔔 Komenda testowa
@slash_command(
    name="ping",
    description="Responds with pong!"
)
async def ping(ctx: CommandContext):
    await ctx.send("Pong!")

# 🔢 Funkcja DM EXP
def licz_exp_dla_dm(levels, sesje=1):
    sredni_poziom = sum(levels) / len(levels)
    exp_dm = (-3702.80688 + 120.71911 * math.exp(((sredni_poziom + 39.19238) / 11.64262))) * sesje
    return round(exp_dm), round(sredni_poziom, 2)

# 🔢 Funkcja gracz EXP
def licz_exp_gracza(level_gracza, level_sredni, exp_dm):
    mod = level_gracza - level_sredni
    reduction = -0.0125 * (mod ** 2 + 1)
    multiplier = 1.0125 + reduction
    exp = round(exp_dm * multiplier)
    return exp

# 📘 Slash command do EXP
@slash_command(
    name="exp",
    description="Oblicz exp dla graczy i DM-a",
    options=[
        SlashCommandOption(
            name="poziomy",
            description="Poziomy graczy oddzielone spacjami, np: 5 6 7",
            type=OptionType.STRING,
            required=True
        )
    ]
)
async def exp(ctx: CommandContext, poziomy: str):
    try:
        poziomy_lista = list(map(int, poziomy.split()))
        if not poziomy_lista:
            await ctx.send("Podaj poziomy graczy, np. /exp poziomy: 5 6 8")
            return

        exp_dm, srednia = licz_exp_dla_dm(poziomy_lista)
        wynik = f"📘 **DM EXP**: {exp_dm} _(dla średniego poziomu {srednia})_\n"
        for i, lv in enumerate(poziomy_lista, start=1):
            exp_gracza = licz_exp_gracza(lv, srednia, exp_dm)
            wynik += f"🎲 Gracz {i} (lv {lv}): {exp_gracza} EXP\n"

        await ctx.send(wynik)
    except Exception as e:
        await ctx.send(f"Błąd: {e}")

# 🔁 Start bota
bot.start()

import discord
from discord.ext import commands
import math

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def licz_exp_dla_dm(levels, sesje=1):
    sredni_poziom = sum(levels) / len(levels)
    exp_dm = (-3702.80688 + 120.71911 * math.exp(((sredni_poziom + 39.19238) / 11.64262))) * sesje
    return round(exp_dm), round(sredni_poziom, 2)

def licz_exp_gracza(level_gracza, level_sredni, exp_dm):
    mod = level_gracza - level_sredni
    reduction = -0.0125 * (mod ** 2 + 1)
    multiplier = 1.0125 + reduction
    exp = round(exp_dm * multiplier)
    return exp

@bot.command()
async def exp(ctx, *args):
    try:
        poziomy = list(map(int, args))
        if not poziomy:
            await ctx.send("Podaj poziomy graczy, np. `!exp 5 6 8`")
            return

        exp_dm, srednia = licz_exp_dla_dm(poziomy)
        wynik = f"📘 **DM EXP**: `{exp_dm}` _(dla średniego poziomu {srednia})_\n"
        for i, lv in enumerate(poziomy, start=1):
            exp = licz_exp_gracza(lv, srednia, exp_dm)
            wynik += f"🎲 Gracz {i} (lv {lv}): `{exp}` EXP\n"

        await ctx.send(wynik)
    except Exception as e:
        await ctx.send(f"Błąd: {e}")

bot.run("MTQwMTIzMjk4MDAyMTc0MzY0Ng.GWINqy.n583kXXFQvQuOVUS0CB31iKEu6WXk48EQ_3utQ")
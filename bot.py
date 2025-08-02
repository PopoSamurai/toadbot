import interactions
import math
import os

bot = interactions.Client(token=os.getenv("DISCORD_TOKEN"))

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

@bot.command(
    name="exp",
    description="Oblicza EXP dla graczy i DM na podstawie poziomów",
    options=[
        interactions.Option(
            name="poziomy",
            description="Poziomy graczy, np. 5 6 8",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def exp(ctx: interactions.CommandContext, poziomy: str):
    try:
        poziomy_lista = list(map(int, poziomy.split()))
        if not poziomy_lista:
            await ctx.send("Podaj poziomy graczy, np. `/exp poziomy: 5 6 8`")
            return

        exp_dm, srednia = licz_exp_dla_dm(poziomy_lista)
        wynik = f"📘 **DM EXP**: `{exp_dm}` _(dla średniego poziomu {srednia})_\n"
        for i, lv in enumerate(poziomy_lista, start=1):
            exp_gracza = licz_exp_gracza(lv, srednia, exp_dm)
            wynik += f"🎲 Gracz {i} (lv {lv}): `{exp_gracza}` EXP\n"

        await ctx.send(wynik)
    except Exception as e:
        await ctx.send(f"Błąd: {e}")

bot.start()
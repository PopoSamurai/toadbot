import os
import math
from dotenv import load_dotenv
from interactions import Client, CommandContext, slash_command, OptionType, option

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

bot = Client(token=token)

def licz_exp_dla_dm(levels, sesje=1):
    sredni_poziom = sum(levels) / len(levels)
    exp_dm = (-3702.80688 + 120.71911 * math.exp(((sredni_poziom + 39.19238) / 11.64262))) * sesje
    return round(exp_dm), round(sredni_poziom, 2)

def licz_exp_gracza(level_gracza, level_sredni, exp_dm):
    mod = level_gracza - level_sredni
    reduction = -0.0125 * (mod ** 2 + 1)
    multiplier = 1.0125 + reduction
    return round(exp_dm * multiplier)

@slash_command(name="ping", description="Sprawdza czy bot działa")
async def ping(ctx: CommandContext):
    await ctx.send("Pong!")

@slash_command(name="exp", description="Oblicz exp dla graczy i DM-a")
@option()
async def exp(
    ctx: CommandContext,
    poziomy: str = option(
        description="Poziomy graczy oddzielone spacjami, np: 5 6 7",
        required=True,
        opt_type=OptionType.STRING,
    )
):
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

bot.start()

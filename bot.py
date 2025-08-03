import interactions
import os

# Upewniamy się, że token jest zaciągany z systemowego środowiska
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("Brak DISCORD_TOKEN w środowisku!")

bot = interactions.Client(token=token)


# Komenda kalkulatora exp (przykładowa)
@bot.command(
    name="exp",
    description="Oblicza exp potrzebny do poziomu",
    options=[
        interactions.Option(
            name="poziom",
            description="Poziom docelowy",
            type=interactions.OptionType.INTEGER,
            required=True,
        )
    ],
)
async def exp(ctx: interactions.CommandContext, poziom: int):
    # Przykład prostego wzoru
    if poziom < 1:
        await ctx.send("Poziom musi być większy niż 0!")
        return
    exp = sum([i * 100 for i in range(1, poziom + 1)])
    await ctx.send(f"Aby osiągnąć poziom {poziom}, potrzebujesz {exp} punktów doświadczenia.")


bot.start()

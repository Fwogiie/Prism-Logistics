import nextcord
from PrismBot import bot

@bot.command(name="echo")
async def echo(ctx, arg):
    await ctx.send(arg)

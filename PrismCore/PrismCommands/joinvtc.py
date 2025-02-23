from PrismBot import bot

@bot.command(name="join")
async def join_vtc(ctx):
    await ctx.send("Are you interested in joining our VTC?\n\nThen apply on the TruckersMP website\nAnd then you can also apply in <#1342827168786288650>")
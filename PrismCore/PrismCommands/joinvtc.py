from PrismBot import bot
import nextcord

@bot.command(name="join")
async def join_vtc(ctx):
    embed = nextcord.Embed(title="Are you interested in joining our VTC?",
                           description="Then apply on the [TruckersMP website](https://truckersmp.com/vtc/78375/)\nThen apply in <#1342827168786288650>",
                           color=nextcord.Color.purple())
    await ctx.send(embed=embed)
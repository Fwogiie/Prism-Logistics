from PrismBot import bot
import nextcord

@bot.command(name="jobtracker")
async def truckershub_download(ctx):
    embed = nextcord.Embed(title="TruckersHub job tracker",
                           description="You can download the TruckersHub tracker [here](https://truckershub.in/download)",
                           color=nextcord.Color.purple())
    await ctx.send(embed=embed)
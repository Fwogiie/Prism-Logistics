from PrismBot import bot

@bot.command(name="jobtracker")
async def truckershub_download(ctx):
    await ctx.send("You can download the TruckersHub tracker [here](https://truckershub.in/download)")
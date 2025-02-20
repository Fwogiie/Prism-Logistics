from PrismBot import bot

# THE join message
async def joinmessage(user):
    joinmessage = f"Welcome {user.mention}\nPlease verify in <#1342216586412687390> to gain access to the server!"
    await bot.get_channel(1342216544440156302).send(joinmessage)

# Triggering the joinmessage
@bot.event
async def on_member_join(member):
    await joinmessage(member)

# Test command
@bot.command(name="joinmessage")
async def joinmessage_test(ctx):
    if ctx.author.id == bot.owner_id:
        await joinmessage(ctx.author)
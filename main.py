from PrismBot import bot
import tokens
# Setup handler
import PrismBot
import PrismCore
import PrismCore.joinmessage
import PrismCore.verification

bot.load_extension("onami")

# Further Setup
@bot.event
async def on_ready():
    # Setup Verification
    await PrismCore.verification.startup_logic()


# Bot starter
bot.run(tokens.token)
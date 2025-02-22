from PrismBot import bot
import tokens
# Setup handler
import PrismBot
import PrismCore
import PrismCore.joinmessage
import PrismCore.verification
import PrismCore.driver_apps

bot.load_extension("onami")

# Further Setup
@bot.event
async def on_ready():
    # Setup Verification
    await PrismCore.verification.startup_logic()
    # Setup Driver Applications
    await PrismCore.driver_apps.startup_logic()


# Bot starter
bot.run(tokens.token)
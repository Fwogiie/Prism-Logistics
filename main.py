from PrismBot import bot
import tokens
# Setup handler
import PrismBot
import PrismCore
import PrismCore.joinmessage
import PrismCore.verification
import PrismCore.driver_apps
import PrismCore.event_invite
import PrismCore.PrismCommands.truckershubdownload
import PrismCore.PrismCommands.joinvtc
import PrismCore.PrismCommands.create_convoy_event

bot.load_extension("onami")

# Further Setup
@bot.event
async def on_ready():
    # Setup Verification
    await PrismCore.verification.startup_logic()
    # Setup Driver Applications
    await PrismCore.driver_apps.startup_logic()
    # Setup Event invitations
    await PrismCore.event_invite.startup_logic()

# Bot starter
bot.run(tokens.token)
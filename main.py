from PrismBot import bot
import tokens
# Setup handler
import PrismBot
import PrismCore
import PrismCore.PrismCommands.test

bot.load_extension("onami")

# Bot starter
bot.run(tokens.token)
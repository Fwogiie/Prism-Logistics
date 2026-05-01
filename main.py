from SideBot import bot
import tokens
# Setup handler
import SideBot
import CampysCore
import CampysCore.CampysCommands
import CampysCore.CampysCommands.corposays

bot.load_extension("onami")

# Bot starter
bot.run(tokens.token)
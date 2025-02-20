import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",
                   intents=intents,
                   owner_id=785037540155195424)
print(f"{__name__} loaded in.")
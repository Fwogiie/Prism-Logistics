import PrismCore.variables
from PrismBot import bot
import nextcord

async def verifybutton():
    # Button trigger logic
    async def button_callback(ctx) :
        await ctx.user.add_roles(bot.get_guild(1334535876885221407).get_role(1342223884182880326))
    button = nextcord.ui.Button(label="Verify", style=nextcord.ButtonStyle.green)
    button.callback = button_callback
    # Make a viewable view
    view = nextcord.ui.View()
    view.add_item(button)
    return view

async def startup_logic():
    verifymessage = await bot.get_channel(1342216586412687390).fetch_message(1342221890256633987)
    embed = nextcord.Embed(title="Verification", description="Click the button below to verify!")
    embed.set_thumbnail(PrismCore.variables.prism_logo_1024)
    await verifymessage.edit(embed=embed, view=await verifybutton())

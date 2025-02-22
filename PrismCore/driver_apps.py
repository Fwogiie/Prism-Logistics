import nextcord
import PrismCore.variables
from PrismBot import bot

async def application_handler(user: dict):
    # Create embed and add application values
    embed = nextcord.Embed(title="Driver Application", color=nextcord.Color.purple())
    embed.set_thumbnail(PrismCore.variables.prism_logo_1024)
    embed.add_field(name="TMP Profile:", value=f"[{user['TmpId']}](https://truckersmp.com/user/{user['TmpId']})",
                    inline=False)
    embed.add_field(name="Age:", value=user["Age"], inline=False)
    embed.add_field(name="Introduction:", value=user["Bio"], inline=False)
    embed.add_field(name="Other VTCs?:", value=user["OtherVtcs"], inline=False)
    embed.add_field(name="How did you find us?", value=user["FoundFrom"], inline=False)
    userthread = await bot.get_channel(1342827168786288650).create_thread(name=str(user["TmpId"]), type=nextcord.ChannelType(value=12))
    await userthread.send(f"<@{user['DiscordId']}> <@&1342827639894970428>", embed=embed)
    return userthread.id


async def applybutton():
    # Button Trigger logic
    async def button_callback(ctx):
        # Modal Trigger logic
        async def modal_callback(ctx):
            #
            user["TmpId"] = int(tmpuser.value.split("/user/")[1])
            user["DiscordId"] = ctx.user.id
            user["Age"] = int(howold.value)
            user["Bio"] = bio.value
            user["OtherVtcs"] = othervtcs.value
            user["FoundFrom"] = foundfrom.value
            threadid = await application_handler(user)
            await ctx.send(f"Thank you for applying!! We will be answering you in <#{threadid}> !", ephemeral=True)
        # Make a modal
        modal = nextcord.ui.Modal(title="Driver Application", auto_defer=True)
        # Make the modal fields
        tmpuser = nextcord.ui.TextInput(label="TMP Profile link", required=True, placeholder="Eg. https://truckersmp.com/user/5307161")
        howold = nextcord.ui.TextInput(label="How old are you?", required=True, max_length=2)
        bio = nextcord.ui.TextInput(label="Tell us more about yourself!", style=nextcord.TextInputStyle.paragraph,
                                    required=True, placeholder="Eg. What your hobbies are, Etc etc..")
        othervtcs = nextcord.ui.TextInput(label="Have you been in other VTCs?",
                                          placeholder="If so: Which ones?\nLeave blank if you have not been in other VTCs.",
                                          style=nextcord.TextInputStyle.paragraph, required=False)
        foundfrom = nextcord.ui.TextInput(label="How did you find us?", placeholder="Eg. In-Game ad, Friend invite", required=True)
        # Add fields to modal
        modal.add_item(tmpuser)
        modal.add_item(howold)
        modal.add_item(bio)
        modal.add_item(othervtcs)
        modal.add_item(foundfrom)
        # Set modal callback
        modal.callback = modal_callback
        # Send the modal when the apply button gets pressed
        await ctx.response.send_modal(modal)
        # Make a user application dict
        user = {}
    button = nextcord.ui.Button(label="Apply", style=nextcord.ButtonStyle.green)
    button.callback = button_callback
    # Make a viewable view
    view = nextcord.ui.View()
    view.add_item(button)
    return view

async def startup_logic():
    # Fetch the application message on startup
    applymessage = await bot.get_channel(1342827168786288650).fetch_message(1342827355395199058)
    # Embed to make it all look nice :3
    embed = nextcord.Embed(title="Application",
                           description="Apply to become a Prism logistics driver using the button below!",
                           color=nextcord.Color.purple())
    embed.set_thumbnail(PrismCore.variables.prism_logo_1024)
    await applymessage.edit(embed=embed, view=await applybutton())
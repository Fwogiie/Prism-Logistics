import nextcord
import PrismCore.variables
from PrismBot import bot
import requests
import json

async def acceptbutton():
    async def button_callback(ctx):
        # Check if the user is a recruiter.
        for role in ctx.user.roles:
            if role.id == 1342827639894970428:
                tmpid = str(ctx.channel.name).split(":")[0]
                request = requests.get(f"https://api.truckersmp.com/v2/player/{tmpid}")
                tmpuser = json.loads(request.content)
                if tmpuser["response"]["vtc"]["id"] != 78375:
                    await ctx.channel.send("User is not in VTC. cannot proceed.")
                    return
                # Fetch driver role
                guild = bot.get_guild(1334535876885221407)
                driverrole = guild.get_role(1334562817776549899)
                # Give the user the driver role.
                discordid = str(ctx.channel.name).split(":")[1]
                await guild.get_member(int(discordid)).add_roles(driverrole)
                await bot.get_channel(1334567263780601939).send(f"Everyone please welcome <@{discordid}> as a Prism Logistics Driver!")
    # Make button
    button = nextcord.ui.Button(label="Continue", style=nextcord.ButtonStyle.green)
    button.callback = button_callback
    # Make a viewable view
    view = nextcord.ui.View()
    view.add_item(button)
    return view

@bot.command(name="accept")
async def accept_application(ctx):
    # Check if the user is a recruiter.
    for role in ctx.author.roles:
        if role.id == 1342827639894970428:
            # Make the confirmation embed.
            embed = nextcord.Embed(title="Application Acceptance", description="Are you sure you wish to proceed? There are a few things required before proceeding.\n"
                                                                               "Please make sure the user has downloaded and installed TruckersHub, and that the user is above 16 of age.\n"
                                                                               "When those requirements are met, you may proceed with the button below.",
                               color=nextcord.Color.purple())
            await ctx.send(embed=embed, view=await acceptbutton())
            return

@bot.command(name="deny")
async def deny_application(ctx):
    pass

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
    userthread = await bot.get_channel(1342827168786288650).create_thread(name=f"{user['TmpId']}:{user['DiscordId']}", type=nextcord.ChannelType(value=12))
    await userthread.send(f"<@{user['DiscordId']}> <@&1342827639894970428>", embed=embed)
    request = requests.get(f"https://api.truckersmp.com/v2/player/{user['TmpId']}")
    tmpuser = json.loads(request.content)
    if tmpuser["error"] is False:
        if tmpuser["response"]["bansCount"] > 1:
            await userthread.send("User has more than 1 active ban. This is an automatic Rejection.")
    else:
        await userthread.send(f"User's TMP ID was not found.\n```json\n{tmpuser}```\nPlease check for errors.")
    await userthread.send("Please wait as we review your application!")
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
    view = nextcord.ui.View(timeout=None)
    view.add_item(button)
    return view

async def startup_logic():
    # Fetch the application message on startup
    applymessage = await bot.get_channel(1342827168786288650).fetch_message(1342827355395199058)
    # Embed to make it all look nice :3
    embed = nextcord.Embed(title="Application",
                           description="Apply to become a Prism Logistics driver using the button below!",
                           color=nextcord.Color.purple())
    embed.set_thumbnail(PrismCore.variables.prism_logo_1024)
    await applymessage.edit(embed=embed, view=await applybutton())
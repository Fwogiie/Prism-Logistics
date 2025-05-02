from PrismBot import bot
import nextcord
import PrismCore.variables
import json
import requests

# Startup logic triggered when the bot boots up!
async def startup_logic():
    # Fetch the event invitation message on startup
    applymessage = await bot.get_channel(1363139620430156038).fetch_message(1363889111265574982)
    # Embed to make it all look nice :3
    embed = nextcord.Embed(title="Event Invitations",
                           description="Click the button bellow to invite us to your event!",
                           color=nextcord.Color.purple())
    embed.set_thumbnail(PrismCore.variables.prism_logo_1024)
    await applymessage.edit("", embed=embed, view=await invitebutton())

async def invitationhandler(event: dict):
    # Create embed and add application values
    embed = nextcord.Embed(title="Event Invitation", description=event["pasted"], color=nextcord.Color.purple())
    embed.set_thumbnail(PrismCore.variables.prism_logo_1024)
    embed.add_field(name="TMP Event:", value=event['tmpEvent'],
                    inline=False)
    embed.add_field(name="Position:", value=event["vtcPosition"], inline=False)
    tmpeventreq = requests.get(f"https://api.truckersmp.com/v2/events/{event['tmpEvent'].split('/events/')[1]}")
    if tmpeventreq.status_code != 200:
        print(f"Unexpected Error: {tmpeventreq.status_code}\n{tmpeventreq.content}")
        return
    tmpeventresp = json.loads(tmpeventreq.text)
    invitethread = await bot.get_channel(1363139620430156038).create_thread(name=tmpeventresp["response"]["name"], type=nextcord.ChannelType(value=12))
    await invitethread.send(f"<@{event['discordId']}> <@&1363909930016309509>", embed=embed)
    await invitethread.send("We will be answering your invitation shortly!")
    return invitethread.id

async def invitebutton():
    # Button Trigger logic
    async def button_callback(ctx):
        # Log the usage
        print(f"Reached by {ctx.user.id}")
        # Modal Trigger logic
        async def modal_callback(ctx):
            # Set values
            event["tmpEvent"] = tmpevent.value
            event["vtcPosition"] = vtcpos.value
            event["pasted"] = invitetext.value
            event["discordId"] = str(ctx.user.id)
            threadid = await invitationhandler(event)
            # Log the event URL
            print(tmpevent.value)
            await ctx.send(f"Thank you for inviting us! We will be answering you in <#{threadid}> !", ephemeral=True)
        # Make a modal
        modal = nextcord.ui.Modal(title="Event Invitation", auto_defer=True)
        # Make the modal fields
        tmpevent = nextcord.ui.TextInput(label="TMP event link", required=True, placeholder="Eg. https://truckersmp.com/events/1")
        vtcpos = nextcord.ui.TextInput(label="What's' your position in the VTC?", required=True)
        invitetext = nextcord.ui.TextInput(label="Pasted Invitation", required=False, style=nextcord.TextInputStyle.paragraph)
        # Add fields to modal
        modal.add_item(tmpevent)
        modal.add_item(vtcpos)
        modal.add_item(invitetext)
        # Set modal callback
        modal.callback = modal_callback
        # Send the modal when the apply button gets pressed
        await ctx.response.send_modal(modal)
        # Make a user application dict
        event = {}
    button = nextcord.ui.Button(label="Invite", style=nextcord.ButtonStyle.green)
    button.callback = button_callback
    # Make a viewable view
    view = nextcord.ui.View(timeout=None)
    view.add_item(button)
    return view

async def acceptbutton():
    async def button_callback(ctx):
        # Check if the user is a event team.
        for role in ctx.user.roles:
            if role.id == 1363909930016309509:
                await ctx.message.delete()
                await ctx.channel.send("Thank you for inviting us! We'll make sure to be there!\n\nThis thread may now be closed.")
    # Make button
    button = nextcord.ui.Button(label="Continue", style=nextcord.ButtonStyle.green)
    button.callback = button_callback
    # Make a viewable view
    view = nextcord.ui.View()
    view.add_item(button)
    return view

@bot.command(name="close")
async def accept_invitation(ctx):
    # Check if the user is a event team.
    for role in ctx.author.roles:
        if role.id == 1363909930016309509:
            # Make the confirmation embed.
            embed = nextcord.Embed(title="Invitation Acceptance", description="Are you sure you wish to proceed? There are a few required things before proceeding.\n"
                                                                               "Please make sure we have a __confirmed__ slot along with a slot image. and that the event has been correctly set in the event tab on top.\n"
                                                                               "When those requirements are met, you may proceed with the button below.",
                               color=nextcord.Color.purple())
            await ctx.send(embed=embed, view=await acceptbutton())
            return
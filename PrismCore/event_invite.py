from PrismBot import bot
import nextcord
import PrismCore.variables
import json
import requests
from datetime import datetime

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
    print(tmpeventresp)
    invitethread = await bot.get_channel(1363139620430156038).create_thread(name=tmpeventresp["response"]["name"], type=nextcord.ChannelType(value=12))
    await invitethread.send(f"<@{event['discordId']}> <@&1363909930016309509>", embed=embed)
    await invitethread.send("We will be answering your invitation shortly!")
    # Store the event Invite locally for tools needing it
    with open("PrismCore/PrismStorage/convoys.json", "r") as readFile:
        filecontents = json.loads(readFile.read())
    requireddlcs = ""
    for dlc in tmpeventresp["response"]["dlcs"]:
        requireddlcs += f"{tmpeventresp["response"]["dlcs"][dlc]}, "
    filecontents["eventInvites"][invitethread.id] = {"eventUrl": event['tmpEvent'], "eventName": tmpeventresp["response"]["name"],
                                                     "requiredDlc": requireddlcs, "eventServer": tmpeventresp["response"]["server"]["name"],
                                                     "departure": tmpeventresp["response"]["departure"], "arriving": tmpeventresp["response"]["arrive"],
                                                     "meetupTime": tmpeventresp["response"]["meetup_at"], "startTime": tmpeventresp["response"]["start_at"],
                                                     "eventBannerUrl": tmpeventresp["response"]["banner"], "slot": "", "slotImage": ""}
    with open("PrismCore/PrismStorage/convoys.json", "w") as writeFile:
        json.dump(filecontents, writeFile, indent=2)
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
            # Log the event URL
            print(tmpevent.value)
            threadid = await invitationhandler(event)
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

@bot.slash_command(name="event", description="Event team commands")
async def _event_cmd(ctx):
    # This commands sole purpose is for subcommands :3
    pass

@_event_cmd.subcommand(name="edit", description="Edit current open event invitation")
async def edit_event(ctx):
    # Open the file to fetch current event
    with open("PrismCore/PrismStorage/convoys.json", "r") as readFile:
        filecontents = json.loads(readFile.read())
    try:
        event = filecontents["eventInvites"][str(ctx.channel.id)]
    except KeyError:
        await ctx.send("Could not find event.", ephemeral=True)
        return

    async def modal_callback(ctx):
        event["slot"] = slot.value
        event["slotImage"] = slotimg.value
        filecontents["eventInvites"][str(ctx.channel.id)] = event
        with open("PrismCore/PrismStorage/convoys.json", "w") as writeFile:
            json.dump(filecontents, writeFile, indent=2)
        await ctx.send("Successfully Updated slot information", ephemeral=True)
    # Make a modal
    modal = nextcord.ui.Modal(title="Event Edit", auto_defer=True)
    # Make the modal fields
    slot = nextcord.ui.TextInput(label="Slot", required=False, default_value=event["slot"])
    slotimg = nextcord.ui.TextInput(label="Slot Image", required=False, default_value=event["slotImage"])
    # Add fields to modal
    modal.add_item(slot)
    modal.add_item(slotimg)
    # Set modal callback
    modal.callback = modal_callback
    # Send the modal when the apply button gets pressed
    await ctx.response.send_modal(modal)
    print(event)

@_event_cmd.subcommand(name="preview", description="Preview current open event :3")
async def preview_event(ctx):
    with open("PrismCore/PrismStorage/convoys.json", "r") as readFile:
        filecontents = json.loads(readFile.read())
    try:
        event = filecontents["eventInvites"][str(ctx.channel.id)]
    except KeyError:
        await ctx.send("Could not find event.", ephemeral=True)
        return
    embed = nextcord.Embed(title="Event Preview",
                           color=nextcord.Color.purple(),
                           description=f"- TruckersMP event: {event['eventUrl']}\n- Server: {event['eventServer']}\n"
                                       f"# Departure:\n- Location: {event['departure']['location']}\n- City: {event['departure']['city']}\n"
                                       f"- Our slot: {event['slot']}\n- Slot image: [image]({event['slotImage']})\n"
                                       f"# Arriving:\n- Location: {event['arriving']['location']}\n- City: {event['arriving']['city']}\n"
                                       f"# Requirements:\n- DLCs: {event['requiredDlc']}")
    await ctx.send(embed=embed, ephemeral=True)

@_event_cmd.subcommand(name="accept", description="Accept current open event invitation")
async def accept_event(ctx):
    await ctx.response.defer()
    with open("PrismCore/PrismStorage/convoys.json", "r") as readFile:
        filecontents = json.loads(readFile.read())
    try:
        event = filecontents["eventInvites"][str(ctx.channel.id)]
    except KeyError:
        await ctx.send("Could not find event.", ephemeral=True)
        return
    if not event["slot"] or not event["slotImage"]:
        await ctx.send("Missing slot values! Please make sure you have both a slot and slot image set in `/event edit`", ephemeral=True)
        return
    filecontents["lastEventId"] += 1
    filecontents["upcomingEvents"][str(filecontents["lastEventId"])] = event
    filecontents["eventInvites"].pop(str(ctx.channel.id))
    with open("PrismCore/PrismStorage/convoys.json", "w") as writeFile:
        json.dump(filecontents, writeFile, indent=2)
    discordevent = await ctx.guild.create_scheduled_event(name=f"{filecontents["lastEventId"]}. {event['eventName']}",
                                           start_time=datetime.fromisoformat(event['meetupTime']),
                                           end_time=datetime.fromisoformat(event['startTime']),
                                           image=requests.get(event['eventBannerUrl']).content,
                                           entity_type=nextcord.ScheduledEventEntityType.external,
                                           metadata=nextcord.EntityMetadata(location="TMP"),
                                           description=f"- TruckersMP event: {event['eventUrl']}\n- Server: {event['eventServer']}\n"
                                                       f"# Departure:\n- Location: {event['departure']['location']}\n- City: {event['departure']['city']}\n"
                                                       f"- Our slot: {event['slot']}\n- Slot image: [image]({event['slotImage']})\n"
                                                       f"# Arriving:\n- Location: {event['arriving']['location']}\n- City: {event['arriving']['city']}\n"
                                                       f"# Requirements:\n- DLCs: {event['requiredDlc']}")
    event_url = f"https://discord.com/events/{ctx.guild.id}/{discordevent.id}"
    await ctx.followup.send(f"[Event]({event_url}) has been created\n\nWe'll make sure to be there! Thank you for inviting us!")
    await ctx.channel.edit(archived=True, locked=True)
    alertchannel = bot.get_channel(1334567209044807826)
    await alertchannel.send(f"Hello <@&1334562817776549899> !\nWe have just gotten a slot for [{event['eventName']}]({event_url})\n"
                            f"I would really appreciate if you could Mark yourself as 'Interested' If you wish to attend that convoy!")




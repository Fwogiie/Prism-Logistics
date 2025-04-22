import urllib.request
from datetime import datetime
import json
import requests
from PrismBot import bot
import nextcord
import base64


@bot.slash_command(name="create")
async def _create(ctx):
    # This does not need any logic as this is meant for subcommands.
    pass

@_create.subcommand(name="convoy", description="DLCs should be separated with '-'")
async def _create_convoy(ctx, discord_event_id: str, convoy_url: str, slot: str, slot_img: str, required_dlcs: str="None"):
    await ctx.response.defer()
    discord_event = bot.get_scheduled_event(int(discord_event_id))
    req = requests.get(f"https://api.truckersmp.com/v2/events/{convoy_url.split('/events/')[1]}")
    if req.status_code != 200:
        await ctx.send(f"Unexpected status code! {req.status_code}")
        return
    req = json.loads(req.text)["response"]
    await discord_event.edit(name=req["name"],
                             description=f"- TruckersMP event: {convoy_url}\n- Server: {req['server']['name']}\n"
                                         f"# Departure:\n- Location: {req['departure']['location']}\n- City: {req['departure']['city']}\n"
                                         f"- Our slot: {slot}\n- Slot image: [image]({slot_img})\n"
                                         f"# Arriving:\n- Location: {req['arrive']['location']}\n- City: {req['arrive']['city']}\n"
                                         f"# Requirements:\n- DLCs: {required_dlcs}",
                             start_time=datetime.fromisoformat(req['meetup_at']), end_time=datetime.fromisoformat(req['start_at']),
                             image=requests.get(req['banner']).content)
    await ctx.followup.send("Successfully edited event!")
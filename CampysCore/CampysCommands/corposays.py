import json
import os
from random import randint

import nextcord
import requests
import tokens
from PrismBot import bot


jobs = ['Coal', 'Iron', 'Logs', 'Cement', 'Concrete', 'Limestone', 'Fuel', 'Crude Oil', 'Milk', 'Container', 'Toys',
        'Cheese', 'Bread', 'Sand', 'Plastics', 'Pickup Trash', 'Empty Gapa Farms', 'Wrecked vehicles', 'Quicklime', 'Police love', 'Planks']

jobsdelivery = {"Coal": ["Gwangjin Coal Storage", "Steel Mill Steel Coil Coal Drop", "Steel Mill H-Beam Coal Drop"],
                "Iron": ["Gwangjin Iron Ore Storage", "Steel Mill Steel Coil Iron Ore Drop", "Steel Mill H-Beam Iron Ore Drop"],
                "Logs": ["Sangdo Lumbermil Drop Off", "Migeum Log Warehouse (doing a 50 20ft logs contract)", "Migeum Log Warehouse (doing a 20 12ft logs contract)"],
                "Cement": ["Seongsan Concrete Factory Cement Drop"],
                "Concrete": ["Gwangjin Town Construction Site #1", "Gwangjin Construction Site F1"],
                "Limestone": ["Steel Mill Steel Coil Limestone Drop", "Steel Mill H-Beam Limestone Drop", "Nobong Cement Factory Limestone Drop", "Nobong Quicklime Factory Limestone Drop"],
                "Fuel": ["Seongsan Concrete Factory Fuel Drop", "Migeum Log Warehouse", "Noksan Fuel Storage"],
                "Crude Oil": ["Sanho Oil Refinery"],
                "Milk": ["Daily Cheese Inc. Milk Drop"],
                "Container": ["Sanho Oil Refinery"],
                "Toys": ["Gwangjin Supermarket"],
                "Cheese": ["Gwangjin Supermarket", "Gangjung Supermarket"],
                "Bread": ["Gwangjin Supermarket", "Gangjung Supermarket"],
                "Sand": ["Concrete Factory Sand Dump"],
                "Plastics": ["Toy Factory"],
                "Pickup Trash": ["in* Gwangjin", "in* GangJung", "in* Jeju"],
                "Empty Gapa Farms": ["Gangjung Warehouse", "Jeju Warehouse", "Sinchang Warehouse", "Oji Gate Warehouse"],
                "Wrecked vehicles": ["... Anywhere really xD"],
                "Quicklime": ["Gapa Farms", "Main island Farms"],
                "Police love": ["Main island towns", "Bottom island towns"],
                "Planks": ["Gwangjin Construction Site 1", "Oji Drilling", "Gwangjin Construction Site F1"]}

@bot.slash_command(name="corpo", guild_ids=[1404474707071209502])
async def _corpo(ctx):
    pass

@_corpo.subcommand(name="says", description="Generate a job to do together with corpo members!")
async def _corposays(ctx):
    randomnumber = json.loads(requests.post("https://api.random.org/json-rpc/4/invoke", json={"jsonrpc": "2.0", "method": "generateSignedIntegers", "id": 1, "params": {"apiKey": tokens.randokey, "n": 1, "min": 1, "max": len(jobs), "replacement": False}}).text)["result"]["random"]["data"][0]
    pickedjob = jobs[randomnumber-1]
    delivery = jobsdelivery[pickedjob][randint(0, len(jobsdelivery[pickedjob])-1)]
    await ctx.send(f"Corpo wants you to deliver some **{pickedjob}** to **{delivery}**, get to work!")

@_corposays.subcommand(name="list", description="Show the current jobs that you are able to be given")
async def _corposaysjoblist(ctx):
    joblist = "The current jobs present in the list are:\n\n"
    for x in jobs:
        joblist += f"**{x}** to **{str(jobsdelivery[x]).strip("[]")}**\n\n"
    embed = nextcord.Embed(title="Job list", description=joblist, color=nextcord.Color.purple())
    await ctx.send(embed=embed)
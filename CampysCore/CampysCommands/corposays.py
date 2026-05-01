import json
import os
from random import randint

import nextcord
import requests
import tokens
from SideBot import bot


jobs = ['Coal', 'Iron', 'Logs', 'Cement', 'Concrete', 'Limestone', 'Fuel', 'Crude Oil', 'Milk', 'Containers', 'Toys',
        'Cheese', 'Bread', 'Sand', 'Plastics', 'Quicklime', 'Planks']

jobs_easy = ['Logs', 'Cement', 'Concrete', 'Fuel', 'Crude Oil', 'Milk', 'Containers', 'Toys',
             'Cheese', 'Bread', 'Sand', 'Plastics', 'Quicklime', 'Planks']

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
                "Quicklime": ["Gapa Farms", "Main island Farms"],
                "Planks": ["Gwangjin Construction Site 1", "Oji Drilling", "Gwangjin Construction Site F1", "Gwangjin Coal Mine"]}

jobsdelivery_easy = {
                "Logs": ["Sangdo Lumbermil Drop Off", "Migeum Log Warehouse (doing a 50 20ft logs contract)", "Migeum Log Warehouse (doing a 20 12ft logs contract)"],
                "Cement": ["Seongsan Concrete Factory Cement Drop"],
                "Fuel": ["Seongsan Concrete Factory Fuel Drop", "Migeum Log Warehouse", "Noksan Fuel Storage"],
                "Crude Oil": ["Sanho Oil Refinery"],
                "Milk": ["Daily Cheese Inc. Milk Drop"],
                "Container": ["Sanho Oil Refinery"],
                "Cheese": ["Gangjung Supermarket"],
                "Bread": ["Gangjung Supermarket"],
                "Sand": ["Concrete Factory Sand Dump"],
                "Plastics": ["Toy Factory"],
                "Quicklime": ["Gapa Farms", "Main island Farms"]}

deliverylocations = ['Gwangjin Storage', 'Steel Mill', 'Sangdo Lumbermill', 'Migeum Log Warehouse',
                     'Seongsan Concrete Factory', 'Gwangjin Town Construction Site #1', 'Gwangjin Construction Site F1',
                     'Nobong Cement Factory', 'Noksan', 'Sanho Oil Refinery', 'Daily Cheese Inc.', 'Gwangjin Supermarket',
                     'Gangjung Supermarket', 'Concrete Factory', 'Toy Factory', 'Gapa Farms', 'Oji Drilling',
                     'Gwangjin Coal Mine', 'Gwangjin Iron Mine']

deliverylocations_easy = ['Sangdo Lumbermill', 'Seongsan Concrete Factory',
                          'Nobong Cement Factory', 'Noksan', 'Sanho Oil Refinery', 'Daily Cheese Inc.',
                          'Gangjung Supermarket', 'Concrete Factory', 'Toy Factory', 'Gapa Farms', 'Oji Drilling']

def _true_random_list(list:[]):
    randomnumber = json.loads(requests.post("https://api.random.org/json-rpc/4/invoke",
                                            json={"jsonrpc": "2.0", "method": "generateSignedIntegers", "id": 1,
                                                  "params": {"apiKey": tokens.randokey, "n": 1, "min": 1,
                                                             "max": len(jobs), "replacement": False}}).text)["result"][
        "random"]["data"][0]
    return list[randomnumber]

@bot.slash_command(name="corpo", guild_ids=[1404474707071209502])
async def _corpo(ctx):
    pass

@_corpo.subcommand(name="says", description="Generate a job to do together with corpo members!")
async def _corposays(ctx, destination: bool, load: bool, gwangjin: bool):
    if destination is True and load is True:
        if gwangjin:
            randompick = _true_random_list(jobs)
            delivery = jobsdelivery[randompick][randint(0, len(jobsdelivery[randompick])-1)]
            await ctx.send(f"Corpo wants you to deliver some **{randompick}** to **{delivery}**, get to work!")
        else:
            randompick = _true_random_list(jobs_easy)
            delivery = jobsdelivery_easy[randompick][randint(0, len(jobsdelivery_easy[randompick]) - 1)]
            await ctx.send(f"Corpo wants you to deliver some **{randompick}** to **{delivery}**, get to work!")
    elif destination is False and load is True:
        randompick = _true_random_list(jobs)
        await ctx.send(f"Corpo wants you to deliver some **{randompick}**, get to work!")

    elif destination is True and load is False:
        if gwangjin:
            randompick = _true_random_list(deliverylocations)
            await ctx.send(f"Corpo wants you to deliver to **{randompick}**, get to work!")
        else:
            randompick = _true_random_list(deliverylocations_easy)
            await ctx.send(f"Corpo wants you to deliver to **{randompick}**, get to work!")

@_corpo.subcommand(name="joblist", description="Show the current jobs that you are able to be given")
async def _corposaysjoblist(ctx):
    joblist = "The current jobs present in the list are:\n\n"
    for x in jobs:
        joblist += f"**{x}** to **{str(jobsdelivery[x]).strip("[]")}**\n\n"
    embed = nextcord.Embed(title="Job list", description=joblist, color=nextcord.Color.purple())
    await ctx.send(embed=embed)
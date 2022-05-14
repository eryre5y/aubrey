#!/usr/bin/env python3
import dstk
import discord
from discord.ext import commands

client = commands.Bot(command_prefix = '>')

@client.event
async def on_ready():
    print('aubrey is ready to kill everyone!')
    
client.run(dstk.token)
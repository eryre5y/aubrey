#!/usr/bin/env python3
from operator import contains
import dstk
import discord
import os
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
from itertools import cycle

# config


intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = '>', intents=intents)
status = cycle(['playing with her mind',
        'sleeping',
        'passing away',
        'walking',
        'calming in the church'])

for f in os.listdir("./cogs"):
	if f.endswith(".py"):
		client.load_extension(f'cogs.{f[:-3]}')

# commands

@client.command()
@has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'loaded `{extension}`')
    
@client.command()
@has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'unloaded `{extension}`')
    
@client.command()
@has_permissions(administrator=True)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'reloaded `{extension}`')

@client.command()
async def ping(ctx):
    await ctx.send(f'pong ({round(client.latency * 1000)}ms)')
            
@client.command()
async def text(ctx, *, text):
    await ctx.send(embed=discord.Embed(description=text, color=discord.Color.red()))
    
'''
def is_it_me(ctx):
    return ctx.author.id == 339654527550750720

@client.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send(f'hi im {ctx.author}')
'''


# tasks

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

# events
    
# start msg

@client.event
async def on_ready():
    change_status.start()
    print('aubrey is ready to kill everyone!')
client.run(dstk.token)
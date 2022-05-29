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

client.remove_command("help")

for f in os.listdir("./cogs"):
	if f.endswith(".py"):
		client.load_extension(f'cogs.{f[:-3]}')

# commands

@client.command()
@commands.guild_only()
@has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'loaded `{extension}`')
    
@client.command()
@commands.guild_only()
@has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'unloaded `{extension}`')
    
@client.command()
@commands.guild_only()
@has_permissions(administrator=True)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'reloaded `{extension}`')

@client.command()
async def ping(ctx):
    await ctx.send(embed=discord.Embed(description=f'pong ({round(client.latency * 1000)}ms)', color=discord.Color.purple()))
            
@client.command()
@commands.guild_only()
async def text(ctx, *, text):
    await ctx.send(embed=discord.Embed(description=text, color=discord.Color.red()))
    
@client.command()
@commands.guild_only()
async def help(ctx):
    await ctx.send(embed=discord.Embed(
        description=f"""
        **>help** - help menu \n
        `admin tools` \n
            **>ban <person by mention> <reason>** - ban person \n
            **>unban <member>** - unban person
            **>kick <person by mention> <reason>** - kick person\n
            **>clear <count>** - clear last messages with specific count \n
            **>clearall** - clear all messages in channel (To confirm type "Yes, do as I say.")\n
            **>setmoney <person by mention> <amount>** - set specific money to person \n
            **>load <module>** - load module to bot \n 
            **>unload <module>** - unload module from bot \n 
            **>reload <module>** - reload module in bot \n 
        `money commands` \n
            **>balance** - shows ur current balance \n
            **>reset** - reset ur stats or register in database if you don't exist (to confirm type ">reset confirm") \n
            **>transfer <person> <amount>** - transfer specific money to person \n
        `games` \n
            **>8ball <question>** - predicts your answer \n
            **>casino <bet>** - las vegas casino \n
            **>coin <bet>** - 50/50 chance of winning \n
            **>mine** - earn clams by spamming this command \n
            **>roll <number> <bet>** - roll dice \n
            **>rps <item> <bet>** - rock/paper/scissors game \n
        `music` \n
            **>join** - join voice channel
            **>leave** - leave voice channel
            **>play <url>** - play music without queue
            **>play_queue** - play queued music
            **>pause** - pause music
            **>resume** - resume music
            **>stop** - stop music
            **>queue <url>** - add music to queue (>queue clear to clear queue)
        `other`
            **>ping** - api delay in ms \n 
            **>text** - ur message from bot \n 
            
        questions and suggestions here **something#8653 (user id: 339654527550750720)**
        """,
        color=discord.Color.teal()))
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
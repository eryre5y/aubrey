#!/usr/bin/env python3
import dstk
import discord
import random
from discord.ext import commands

client = commands.Bot(command_prefix = '>')

@client.command()
async def ping(ctx):
    await ctx.send(f'pong ({round(client.latency * 1000)}ms)')
    
@client.command()
async def text(ctx, *, text):
    await ctx.send(text)
    
@client.command(aliases=['8ball', 'eightball'])
async def _8ball(ctx, *, question):
    responses = ['yes.',
                 'no.',
                 'ask urself.',
                 'i don\'t care.',
                 'who knows.',
                 'why do you ask me this?'
                 ]
    await ctx.send(f'{random.choice(responses)}')
# user join/leave

@client.event
async def on_member_join(member):
    print(f'{member} has accepted harakiri.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the world')
    
# start msg

@client.event
async def on_ready():
    print('aubrey is ready to kill everyone!')
    
client.run(dstk.token)
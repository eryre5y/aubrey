#!/usr/bin/env python3
from operator import contains
import dstk
import discord
import random
import os
from discord.ext import commands, tasks
from itertools import cycle

# config

client = commands.Bot(command_prefix = '>')
status = cycle(['playing with her mind',
        'sleeping',
        'passing away',
        'walking',
        'calming in the church'])

# commands

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    
@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'banned {member.mention}')
    
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'unbanned {user.mention}')
            return

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'cleared {amount} messages', delete_after=3)
    
@client.command()
@commands.has_permissions(manage_messages=True)
async def clearall(ctx, *, confirm="no"):
    if confirm == "Yes, do as I say.":
        await ctx.channel.purge(limit=13371337)
        await ctx.send(f'cleared all messages', delete_after=3)
    else:
        await ctx.send(f'to confirm type "Yes, do as I say."')

@client.command()
async def ping(ctx):
    await ctx.send(f'pong ({round(client.latency * 1000)}ms)')
    
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
    
@client.command()
async def casino(ctx):
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    num3 = random.randint(1, 9)
    if num1 == num2 == num3:
        win=":diamond_shape_with_a_dot_inside: Win :sparkler::sparkler::sparkler:"
    else:
        win=":diamond_shape_with_a_dot_inside: Loss"
    await ctx.send(':gem: ' + str(num1) + ' | ' + str(num2) + ' | ' + str(num3) + ' :gem:\n' + str(win))
    
@client.command()
async def roll(ctx):
    await ctx.send(':game_die: ' + str(random.randint(1, 6)) + ' :game_die:')

@client.command()
async def text(ctx, *, text):
    await ctx.send(text)
'''
def is_it_me(ctx):
    return ctx.author.id == 339654527550750720

@client.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send(f'hi im {ctx.author}')
'''

@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

# tasks

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

# events
'''
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('something is wrong i can feel it in my mind')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('i can\'t understand you')
'''
@client.event
async def on_member_join(member):
    print(f'{member} has accepted harakiri.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the world')
    
# start msg

@client.event
async def on_ready():
    change_status.start()
    print('aubrey is ready to kill everyone!')
    
client.run(dstk.token)
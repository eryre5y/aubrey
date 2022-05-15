#!/usr/bin/env python3
from operator import contains
import dstk
import discord
import random
import os
import asyncio
from discord.ext import commands, tasks
import youtube_dl
from dotenv import load_dotenv
from itertools import cycle

# config
load_dotenv()
intents = discord.Intents().all()
musclient = discord.Client(intents=intents)

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

client = commands.Bot(command_prefix = '>', intents=intents)
status = cycle(['playing with her mind',
        'sleeping',
        'passing away',
        'walking',
        'calming in the church'])

# music shit

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

# commands

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'banned {member.mention}')
    
@client.command()
@commands.has_permissions(ban_members=True)
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
    if not ctx.message.author.voice:
        await ctx.send("{} plz join any vc".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
@client.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("i'm not in vc =)")
@client.command()
async def play(ctx,url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=client.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**playing:** {}'.format(filename))
    except:
        await ctx.send("bot isn't in voice channel")
@client.command()
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("bro music isn't playing :skull:")
@client.command()
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("no queue bro :skull:")
@client.command()
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("no music rn")

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
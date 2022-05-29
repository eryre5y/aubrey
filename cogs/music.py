import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from asyncio import sleep
import os

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class Music(commands.Cog):
    
    def __init__(self,client):
        self.client = client
        
        
    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("`music` is online")
        
    #Commands
        
    # source: https://bit.ly/3sKWRs0
    
    @commands.command(pass_cotext=True)
    async def join(self, ctx):
        global vc
        
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        
    @commands.command(pass_context=True)
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        
    @commands.command(pass_context=True)
    async def play(self, ctx, url):
            global vc

            try:
                voice_channel = ctx.message.author.voice.channel
                vc = await voice_channel.connect()
            except:
                print('already connected')

            if vc.is_playing():
                await ctx.send(f'{ctx.message.author.mention}, music is already playing.')

            else:
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)

                URL = info['formats'][0]['url']
                
                if os.name == "nt": 
                    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source = URL, **FFMPEG_OPTIONS))
                else: 
                    vc.play(discord.FFmpegPCMAudio(source = URL, **FFMPEG_OPTIONS))
                while vc.is_playing():
                    await sleep(3)
                if not vc.is_paused():
                    await vc.disconnect()

    @commands.command()
    async def pause(self, ctx):
        if vc.is_playing():
            vc.pause()
            await ctx.send(f"paused music")
        else:
            await ctx.send(f"nothing to pause")

    @commands.command()
    async def resume(self, ctx):
        if vc.is_paused():
            vc.resume()
            await ctx.send(f"resumed")
        else:
            await ctx.send(f"nothing to resume")
        
    @commands.command()
    async def stop(self, ctx):
        if vc.is_playing() or vc.is_paused():
            vc.stop()
            await ctx.send(f"stopped music")
        else:
            await ctx.send(f"music isn't playing rn")
        

        
def setup(client):
    client.add_cog(Music(client))
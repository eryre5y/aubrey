import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from asyncio import sleep
import os

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

queue = []

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
            global queue
            global vc
            try:
                voice_channel = ctx.message.author.voice.channel
                vc = await voice_channel.connect()
            except:
                print('already connected')

            if not queue:

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
            else:
                if vc.is_playing():
                    await ctx.send(f'{ctx.message.author.mention}, music is already playing.')

                else:
                    for url in queue:
                        try:
                            with YoutubeDL(YDL_OPTIONS) as ydl:
                                info = ydl.extract_info(url, download=False)

                            URL = info['formats'][0]['url']
                            
                            if os.name == "nt": 
                                vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source = URL, **FFMPEG_OPTIONS))
                            else: 
                                vc.play(discord.FFmpegPCMAudio(source = URL, **FFMPEG_OPTIONS))
                        except:
                            await ctx.send(f'something is wrong')
                        else:
                            await ctx.send(f'queue done!')
                        
            while vc.is_playing():
                await sleep(30)
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
        
    @commands.command()
    async def queue(self, ctx, url):
        global queue
        
        try:
            queue.append(url)
            await ctx.send(f"added to queue")
        except:
            await ctx.send(f"can't add to queue")

        if url == "clear":
            queue.clear()
            await ctx.send(f"queue cleared!")
        

        
def setup(client):
    client.add_cog(Music(client))
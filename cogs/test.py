import discord
from discord.ext import commands

class Test(commands.Cog):
    
    def __init__(self,client):
        self.client = client
        
    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("`test` is online")
        
    #Commands
    @commands.command()
    async def tping(self, ctx):
        await ctx.send(embed=discord.Embed(description=f'pong ({round(self.client.latency * 1000)}ms)', color=discord.Color.purple()))
        
def setup(client):
    client.add_cog(Test(client))
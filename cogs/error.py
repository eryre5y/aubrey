import discord
from discord.ext import commands

class Error(commands.Cog):
    
    def __init__(self,client):
        self.client = client
        
    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("`error` is online")
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('something is wrong i can feel it in my mind')
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send('i can\'t understand you')
        elif isinstance(error,commands.MissingPermissions):
            await ctx.send('u don\'t have permission >:C')
        
def setup(client):
    client.add_cog(Error(client))
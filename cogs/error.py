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
            await ctx.send(embed=discord.Embed(description = 'something is wrong i can feel it in my mind', color=discord.Color.dark_purple()))
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(embed=discord.Embed(description = 'i can\'t understand you', color=discord.Color.dark_purple()))
        elif isinstance(error,commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(description = 'u don\'t have permission >:C', color=discord.Color.dark_purple()))
        elif isinstance(error, commands.CommandRegistrationError):
            await ctx.send(embed=discord.Embed(description = 'why i can\'t register this? ;(', color=discord.Color.dark_purple()))
        elif isinstance(error, commands.CommandError):
            await ctx.send(embed=discord.Embed(description = 'something\'s wrong with this command :(', color=discord.Color.dark_purple()))
        
def setup(client):
    client.add_cog(Error(client))
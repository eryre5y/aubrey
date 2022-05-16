import discord
from discord.ext import commands
import sqlite3

db = sqlite3.connect('base.db')
cursor = db.cursor()

class Admin(commands.Cog):
    
    def __init__(self,client):
        self.client = client
        
    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("`admin` is online")
        
    #Commands

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'banned {member.mention}')
        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        
        for ban_entry in banned_users:
            user = ban_entry.user
            
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'unbanned {user.mention}')
                return

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'cleared {amount} messages', delete_after=3)
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clearall(self, ctx, *, confirm="no"):
        if confirm == "Yes, do as I say.":
            await ctx.channel.purge(limit=13371337)
            await ctx.send(f'cleared all messages', delete_after=3)
        else:
            await ctx.send(f'to confirm type "Yes, do as I say."')
        
def setup(client):
    client.add_cog(Admin(client))
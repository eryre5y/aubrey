import discord
from discord.ext import commands
import sqlite3

db = sqlite3.connect('base.db')
cursor = db.cursor()

class Database(commands.Cog):
    
    def __init__(self,client):
        self.client = client
        
    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("`database` is online")
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has accepted harakiri.')
        cursor.execute(f"SELECT id FROM users where id={member.id}")
        if cursor.fetchone() == None:
            cursor.execute(f"INSERT INTO users VALUES ({member.id}, 420)")
        else:
            pass
        db.commit()
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left the world')
        
    #Commands
    @commands.command()
    async def reset(self, ctx):
        cursor.execute(f"SELECT id FROM users where id={ctx.author.id}")
        if cursor.fetchone() == None:
            cursor.execute(f"INSERT INTO users VALUES ({ctx.author.id}, 420)")
            db.commit()
        else:
            cursor.execute(f"UPDATE users SET balance = 420 WHERE id = {ctx.author.id}")
            db.commit()
        await ctx.send(f'reset completed')
        
    @commands.command()
    async def balance(self, ctx):
        balance = cursor.execute(f"SELECT balance FROM users where id={ctx.author.id}")
        await ctx.send(embed=discord.Embed(description=f'your balance is {balance.fetchone()[0]} clams', color=discord.Color.blue()))
        
def setup(client):
    client.add_cog(Database(client))
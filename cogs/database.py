import discord
from discord.ext import commands
from discord.ext import commands, tasks
import sqlite3

db = sqlite3.connect('base.db')
cursor = db.cursor()

class Database(commands.Cog):
    
    def __init__(self,client):
        self.client = client
        
    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS users (guild_id INT,
            id INT,
            balance INT
            )""")
        db.commit()
        for guild in self.client.guilds:
            for member in guild.members:
                print(member)
                if cursor.execute(f"SELECT guild_id, id FROM users where guild_id={member.guild.id}").fetchone() != None and cursor.execute(f"SELECT id FROM users where id={member.id} AND guild_id={member.guild.id}").fetchone() != None:
                    pass
                else:
                    cursor.execute(f"INSERT INTO users VALUES ({member.guild.id}, {member.id}, 420)")
                    db.commit()
        print("`database` is online")
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has accepted harakiri.')
        cursor.execute(f"SELECT * FROM users WHERE guild_id={member.guild.id} AND id={member.id}")
        if cursor.fetchone() == None:
            cursor.execute(f"INSERT INTO users VALUES ({member.guild.id}, {member.id}, 420)")
        else:
            pass
        db.commit()
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left the world')
        
    #Commands
    @commands.command()
    @commands.guild_only()
    async def reset(self, ctx, conf):
        if conf == "confirm":
            if cursor.execute(f"SELECT guild_id FROM users where guild_id={ctx.author.guild.id}").fetchone() != None and cursor.execute(f"SELECT id FROM users where id={ctx.author.id}").fetchone() != None:
                cursor.execute(f"UPDATE users SET balance = 420 WHERE id = {ctx.author.id} AND guild_id = {ctx.author.guild.id}")
                db.commit()
                await ctx.send(embed=discord.Embed(description=f'reset completed', color=discord.Color.purple()))
            else:
                cursor.execute(f"INSERT INTO users VALUES ({ctx.author.guild.id}, {ctx.author.id}, 420)")
                db.commit()
        elif conf == None or conf != "confirm":
            await ctx.send(embed=discord.Embed(description=f'please confirm with ">reset confirm"', color=discord.Color.purple()))
        
    @commands.command()
    @commands.guild_only()
    async def balance(self, ctx):
        balance = cursor.execute(f"SELECT balance FROM users WHERE id={ctx.author.id} AND guild_id={ctx.author.guild.id}")
        await ctx.send(embed=discord.Embed(description=f'your balance is {balance.fetchone()[0]} clams', color=discord.Color.purple()))
        
    @commands.command()
    @commands.guild_only()
    async def transfer(self, ctx, member : discord.Member, amount : int):
        balance = cursor.execute(f"SELECT balance FROM users WHERE id={ctx.author.id} AND guild_id={ctx.author.guild.id}").fetchone()[0]
        if balance < amount:
            await ctx.send(embed=discord.Embed(description="insufficient balance", color=discord.Color.purple()))
        else:
            try:
                cursor.execute(f"UPDATE users SET balance = balance - {amount} WHERE id = {ctx.author.id} AND guild_id = {ctx.author.guild.id}")
                cursor.execute(f"UPDATE users SET balance = balance + {amount} WHERE id = {member.id} AND guild_id = {member.guild.id}")
                db.commit()
                await ctx.send(embed=discord.Embed(description=f"transfered {amount} clams to {member}", color=discord.Color.purple()))
            except sqlite3.Error as er:
                await ctx.send(embed=discord.Embed(description=f"transfer failed\nerror: {er}", color=discord.Color.purple()))
    
def setup(client):
    client.add_cog(Database(client))
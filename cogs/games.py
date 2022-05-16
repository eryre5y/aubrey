import discord
from discord.ext import commands, tasks
import random
import sqlite3

db = sqlite3.connect('base.db')
cursor = db.cursor()

class Games(commands.Cog):
    
    def __init__(self,client):
        self.client = client
        
    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("`games` is online")
        
    #Commands
    @commands.command(aliases=['8ball', 'eightball'])
    async def _8ball(self, ctx, *, question):
        responses = ['yes.',
                    'no.',
                    'ask urself.',
                    'i don\'t care.',
                    'who knows.',
                    'why do you ask me this?'
                    ]
        await ctx.send(f'{random.choice(responses)}')
        
    @commands.command()
    async def casino(self, ctx, bet : int):
        balance = cursor.execute(f"SELECT balance FROM users WHERE id={ctx.author.id} AND guild_id={ctx.author.guild.id}").fetchone()[0]
        if balance < bet:
            await ctx.send("insufficient balance")
        else:
            fruits = ("lemon","watermelon","cherries","apple","grapes","strawberry")
            pos1 = fruits[random.randint(0,5)]
            pos2 = fruits[random.randint(0,5)]
            pos3 = fruits[random.randint(0,5)]
            if pos1 == pos2 == pos3:
                win=f":sparkler::sparkler::sparkler: :diamond_shape_with_a_dot_inside: u won {bet * 5} clams :diamond_shape_with_a_dot_inside: :sparkler::sparkler::sparkler:"
                cursor.execute(f"UPDATE users SET balance = balance + {bet * 5} WHERE id = {ctx.author.id} AND guild_id={ctx.author.guild.id}")
                db.commit()
            else:
                win=f":skull: loss (lost {bet} clams) :skull:"
                cursor.execute(f"UPDATE users SET balance = balance - {bet} WHERE id = {ctx.author.id} AND guild_id={ctx.author.guild.id}")
                db.commit()
            await ctx.send(f':gem: :{pos1}: | :{pos2}: | :{pos3}: :gem:\n{win}')
        
    @commands.command()
    async def roll(self, ctx, choice : int, bet : int):
        dice = random.randint(1,6)
        balance = cursor.execute(f"SELECT balance FROM users WHERE id={ctx.author.id} AND guild_id={ctx.author.guild.id}").fetchone()[0]
        if balance < bet:
            await ctx.send("insufficient balance")
        else:
            if choice == dice:
                await ctx.send(f"you won. congrats!\n:game_die: {dice} :game_die:")
                cursor.execute(f"UPDATE users SET balance = balance + {bet * 3} WHERE id = {ctx.author.id} AND guild_id={ctx.author.guild.id}")
                db.commit()
            else:
                await ctx.send(f"aw man u lose\n:game_die: {dice} :game_die:")
                cursor.execute(f"UPDATE users SET balance = balance - {bet} WHERE id = {ctx.author.id} AND guild_id={ctx.author.guild.id}")
                db.commit()
                
    @commands.command()
    async def coin(self, ctx, bet):
        bet = int(bet)
        balance = cursor.execute(f"SELECT balance FROM users WHERE id={ctx.author.id} AND guild_id={ctx.author.guild.id}").fetchone()[0]
        if balance < bet:
            await ctx.send("insufficient balance")
        else:
            res=random.randint(1,100)
            if res <= 50:
                cursor.execute(f"UPDATE users SET balance = balance + {bet} WHERE id = {ctx.author.id} AND guild_id={ctx.author.guild.id}")
                db.commit()
                await ctx.send("you won. congrats!")
            elif res == 50:
                await ctx.send("tie. nothing won")
            else:
                cursor.execute(f"UPDATE users SET balance = balance - {bet} WHERE id = {ctx.author.id} AND guild_id={ctx.author.guild.id}")
                db.commit()
                await ctx.send("aw man u lose")
                
    @commands.command()
    async def rps(self, ctx, item : str, bet : int):
        items = ("rock", "paper", "scissor")
        current = items[random.randint(0,2)]
        if (item == "rock" and current == "scissor") or (item == "paper" and current == "rock") or (item == "scissor" and current == "paper"):
            cursor.execute(f"UPDATE users SET balance = balance + {bet} WHERE id = {ctx.author.id} AND guild_id={ctx.author.guild.id}")
            db.commit()
            await ctx.send("you won. congrats!")
        elif item == current:
            await ctx.send("tie. nothing won")
        else:
            cursor.execute(f"UPDATE users SET balance = balance - {bet} WHERE id = {ctx.author.id} AND guild_id={ctx.author.guild.id}")
            db.commit()
            await ctx.send("aw man u lose")
            
    @commands.command()
    async def mine(self, ctx):
        mine = random.randint(1, 100)
        cursor.execute(f"UPDATE users SET balance = balance + {mine} WHERE id = {ctx.author.id} AND guild_id={ctx.author.guild.id}")
        db.commit()
        await ctx.send(f"you mined {mine} clams")
            
        
def setup(client):
    client.add_cog(Games(client))
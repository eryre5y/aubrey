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
    async def casino(self, ctx):
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
        num3 = random.randint(1, 9)
        if num1 == num2 == num3:
            win=":diamond_shape_with_a_dot_inside: Win :sparkler::sparkler::sparkler:"
        else:
            win=":diamond_shape_with_a_dot_inside: Loss"
        await ctx.send(':gem: ' + str(num1) + ' | ' + str(num2) + ' | ' + str(num3) + ' :gem:\n' + str(win))
        
    @commands.command()
    async def roll(self, ctx):
        await ctx.send(':game_die: ' + str(random.randint(1, 6)) + ' :game_die:')
        
    @commands.command()
    async def coin(self, ctx, bet):
        bet = int(bet)
        balance = cursor.execute(f"SELECT balance FROM users where id={ctx.author.id}").fetchone()[0]
        if balance < bet:
            await ctx.send("insufficient balance")
        else:
            res=random.randint(1,100)
            if res <= 50:
                cursor.execute(f"UPDATE users SET balance = balance + {bet} WHERE id = {ctx.author.id}")
                db.commit()
                await ctx.send("you won. congrats!")
            elif res == 50:
                await ctx.send("tie. nothing won")
            else:
                cursor.execute(f"UPDATE users SET balance = balance - {bet} WHERE id = {ctx.author.id}")
                db.commit()
                await ctx.send("aw man u lose")
        
def setup(client):
    client.add_cog(Games(client))
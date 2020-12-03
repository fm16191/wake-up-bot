import discord
from discord.ext import commands, tasks
from datetime import datetime
from time import sleep
import asyncio

fo = open("token.txt","r")
TOKEN = fo.readlines()[0].replace("\n","")


client = discord.Client()

prefix = "&"
bot = commands.Bot(command_prefix = prefix)


users = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # await setreveil(False,False)
    await loop()

# @bot.command(name = "reveil")
async def reveil(channel, user):
    def check(m):
        return m.author.id == int(user)
    while True:
        print("ok test")
        try:
            msg = await bot.wait_for('message', check = check, timeout = 2)
            await channel.send("ok t'es debout bg passe une bonne journee wsh")
            return
        except asyncio.TimeoutError:
            await channel.send(f"REVEILLE TOI <@{user}>")
        else:
            print("noo")

# @tasks.loop(seconds=5.0)
async def verif_reveil():
    print("ok")
    global users
    current_time = await get_time(datetime.now())
    for user in users:
        channel, time = users[user]
        if time == current_time:
            print("OK")
            await reveil(channel, user)
            del users[user]
            return
    await asyncio.sleep(10)

async def loop():
    # asyncio.sleep(2)
    while True:
        await verif_reveil()


async def get_time(time):
    time = str(time)
    time = time.split(" ")[1].split(":")[:2]
    time[0] = str(int(time[0])+1 % 24)
    return ":".join(time)


@bot.command(name = "setreveil", aliases = ["reveil"])
async def setreveil(ctx, *args):
    global users
    print(datetime.now())
    if len(args) == 0:
        await ctx.send("no args")
        return
    if len(ctx.message.mentions) > 0 :
        user = ctx.message.mentions[0]
        print(args)
        if len(args[1].split(":")) == 2 and len(args[1]) <= 5:
            users[str(user.id)] = (ctx.channel, args[1])
            print("ok")
        else:
            await ctx.send("incorrect format")
            return
    else:
        user = ctx.author
        if len(args[0].split(":")) == 2 and len(args[0]) <= 5:
            users[str(user.id)] = (ctx.channel, args[0])
            print("ok")
        else:
            await ctx.send("incorrect format")
            return
    await ctx.send(f"alarm set for user {user.mention} at {users[str(user.id)][1]} in {ctx.channel.mention}")

bot.run(TOKEN)

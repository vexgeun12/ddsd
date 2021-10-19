import asyncio

import discord
from discord.ext import commands

intents=discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)

# 채널 아이디
channel_id = 887287877912911913 
# 역할 아이디
role_id = 846372304295297065

on_O = []
on_X = []

embed_msg = None


@client.event
async def on_ready():
    
    print("default_ready")
    print(client.user.id)
    await client.change_presence(status=discord.Status.online, activity=discord.Game("검은사막"))

@client.command(pass_context=True, aliases=["공성"])
async def addEmbed(ctx, *args):
    global embed_msg

    Check = False
    for role in ctx.author.roles:
        if(role.id == role_id):
            Check = True
    if(not Check):
        return
    if(ctx.channel.id != channel_id):
        return
    if(embed_msg != None):
        await ctx.send("이미 생성된 공성 현황이 있습니다.")
        return
    embed = discord.Embed(title="공성 현황 / Attendance-Sige",description="", color=0x00aaaa)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name="<공성/SIEGE> 참석(attend)⭕", value="0명", inline=False)
    embed.add_field(name="<공성/SIEGE> 불참(absend)❌", value="0명", inline=False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("⭕")
    await msg.add_reaction("❌")
    embed_msg = msg

@client.command(pass_context=True, aliases=["리스트"])
async def checkReaction(ctx, *args):
    Check = False
    for role in ctx.author.roles:
        if (role.id == role_id):
            Check = True
    if (not Check):
        return
    if (ctx.channel.id != channel_id):
        return
    if(args[0] == "참석"):
        result = "공석 참석 리스트\n"
        for user in on_O:
            result += f"{user.name}\n"
        if (len(on_O) == 0):
            result = "공성 참석자가 없습니다."
        await ctx.send(result)
    if (args[0] == "불참"):
        result = "공성 불참 리스트\n"
        for user in on_X:
            result += f"{user.name}\n"
        if(len(on_X) == 0):
            result = "공성 불참자가 업습니다."
        await ctx.send(result)

@client.command(pass_context = True, aliases=["초기화"])
async def clear(ctx):
    global on_O
    global on_X
    global embed_msg
    Check = False
    for role in ctx.author.roles:
        if (role.id == role_id):
            Check = True
    if (not Check):
        return
    if (ctx.channel.id != channel_id):
        return
    on_O.clear()
    on_X.clear()
    embed_msg = None
    number = 100
    counter = 0
    async for x in ctx.channel.history(limit=number):
        if counter < number:
            await x.delete()
            counter += 1
            await asyncio.sleep(0.8)


@client.event
async def on_reaction_add(reaction, user):
    global on_O
    global on_X

    if(user.id == 881685397304905768):
        return

    emoji = reaction.emoji
    if(reaction.message.id == embed_msg.id):
        if(emoji == "⭕"):
            if(user in on_X):
                on_X.remove(user)
            if (user in on_O):
                on_O.remove(user)
            on_O.append(user)
        if(emoji == "❌"):
            if(user in on_O):
                on_O.remove(user)
            if (user in on_X):
                on_X.remove(user)
            on_X.append(user)
        await reaction.remove(user)
        embed = discord.Embed(title="공성 현황 / Attendance-Sige",description="", color=0x00aaaa)
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.add_field(name="<공성/SIEGE> 참석(attend)⭕", value=f"{len(on_O)}명", inline=False)
        embed.add_field(name="<공성/SIEGE> 불참(absend)❌", value=f"{len(on_X)}명", inline=False)
        await embed_msg.edit(embed=embed)


#토큰
client.run("ODgxNjg1Mzk3MzA0OTA1NzY4.YSwbgw.t9L0DNgU7SzMgv1erpO3ZcT81MU")
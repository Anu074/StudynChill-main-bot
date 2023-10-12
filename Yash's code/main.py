import discord
from discord.ext import commands
from kick import kick
import os
from dotenv import load_dotenv
from vc import join
from vc import leave
import nacl
import asyncio
from info import si
from uptime import uptime
# from addrole import addrole
from banall import kickall
from banall import banall
# from music import play

load_dotenv()

# from music import play_song

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="", intents=intents, help_command=None)
bot.add_command(kick)
bot.add_command(kickall)
bot.add_command(banall)
bot.add_command(join)
bot.add_command(leave)
bot.add_command(si)
bot.add_command(uptime)
# bot.add_command(addrole)
# bot.add_command(play)


#ping command
@bot.command(name="ping")
async def respond_with_ping(ctx):
    ping = bot.latency * 1000
    embed = discord.Embed(title="Ping", description=f"The ping of the bot is {ping:.2f}ms", color=0x7615D1)
    await ctx.send(embed=embed)

#will trigger the bot to reply on these messsages

@bot.event
async def on_message(msg):
    mention = msg.author.mention
    if msg.author.bot:
        return
    # if "hello" in msg.content.lower():
    #   await msg.channel.send(f"Hello {mention}")
    if "bsdk" in msg.content.lower():
        await msg.channel.send(f"Kya be {mention} lawde kya backchodhi krha hai gali matt de ")
    if msg.content.lower() == "vanity":
        link = await msg.channel.create_invite(max_uses=0, max_age=0)
        await msg.channel.send(link)
    # if "<@692074532386897920>" in msg.content:
    #     await msg.channel.send(f"He is the almighty titty lover please wait he will reply!!!")
    if "<@1092903009916289087>" in msg.content :
       await msg.channel.send(f"Yes how may I help you ?")
    if "<@1092903009916289087> hello" in msg.content:
        await msg.channel.send(f"hi how are you ?{mention}")
    if "<@1092903009916289087> i am good wbu ?" in msg.content:
        await msg.channel.send(f"yeah i am also doing fine listning to mahesh dalle")
    if "<@1092903009916289087> call 11g officials" in msg.content:
        await msg.channel.send(f"<@&1120977070030344306>")
    # if "<@770857386343923732>" in msg.content :
    #   await msg.channel.send(f"That IITian is too busy to talk please don't bother him!!")
    await bot.process_commands(msg)

#will print in the terminal that the bot is alive
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="MAHESH DALLE"),
                              status=discord.Status.dnd)
    print(f"{bot.user.name}#{bot.user.discriminator} is alive now!!")

#ban Function
@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'The User has been banned')

#can DM the person present in the server
@bot.command()
@commands.has_permissions(administrator=True)
async def DM(ctx, user: discord.User, *, message):
    try:
        pass
        await user.send(message)
        embed = discord.Embed(title=DM, description=f'The message has been sent :smile:', color=0x7615D1)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send('error')

#Message deleter
# @bot.command()
# async def clear(ctx, amount=0):
#     if amount == 0:
#         fail = await ctx.send("Please enter an amount to delete!")
#         await asyncio.sleep(6)
#         await fail.delete()

#     if amount < 100:
#         await ctx.channel.purge(limit=amount)
#         sucess = await ctx.send(f"{amount} messages has been deleted :white_check_mark: ")  # sending success msg
#         await asyncio.sleep(6)  # wait 6 seconds
#         await sucess.delete()  # deleting the sucess msg

#     else:
#         if amount == 0:
#             fail = await ctx.send("Please enter an amount to delete!")
#             await asyncio.sleep(6)
#             await fail.delete()

#avatar
@bot.command()
async def av(ctx, *, avamember: discord.Member = None):
    userAvatarUrl = avamember.avatar.url
    em = discord.Embed(color=discord.Color.from_rgb(255, 0, 0))
    em.set_image(url=f"{userAvatarUrl}")
    em.set_author(name=f"{avamember}")
    em.set_footer(text=f'Requested by {ctx.message.author}')
    await ctx.send(embed=em)



bot.run(os.getenv('TOKEN'))

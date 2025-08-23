import discord
import aiohttp
from discord.ext import commands
from datetime import datetime
import webserver
import requests
impoort os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # needed for on_member_join
client = commands.Bot(command_prefix='=', intents=intents) 
@client.command()
@commands.has_any_role('moderator','Administrator','Owner')
async def helpme(ctx):
    embed = discord.Embed(
        title="📜 Kuromi XD - Command List",
        description="Here are all my commands. Use `=` before each command!",
        color=discord.Color.purple()
    )

    embed.add_field(name="🛠 Moderation", value="""
    `=ban @user reason` - Ban a user
    `=kick @user reason` - Kick a user
    `=mute @user time` - Mute user for given time
    `=unmute @user` - Unmute a user
    """, inline=False)

    embed.add_field(name="🎉 Fun", value="""
    `=hello` - Say hello
    `=bye` - Say bye
    `=ily` - Love message
    `=joke` - Random joke
    """, inline=False)

    embed.add_field(name="🔊 Voice", value="""
    `=join` - Bot joins your VC
    `=leave` - Bot leaves VC
    """, inline=False)

    embed.set_footer(text="❤️ Kuromi XD loves you!")

    await ctx.send(embed=embed)

@client.event
async def on_ready():
    print("The bot is ready for use")
    print('--------------------------')

@client.command()
async def hello(ctx):
    await ctx.send("Hello, I'm Kuromi XD(a bitchy bot)")

@client.command()
async def bye(ctx):
    await ctx.send("Goodbye, have a good day <3")

@client.event
async def on_member_join(member):
    channel = client.get_channel(1404437300082905128)  # your welcome channel ID
    if not channel:
        print("Channel not found or bot has no access.")
        return

    # Fetch joke from API asynchronously
    async with aiohttp.ClientSession() as session:
        async with session.get("https://v2.jokeapi.dev/joke/Any?type=single") as res:
            data = await res.json()
            joke = data.get("joke", "Couldn't fetch a joke sorry")

    await channel.send(f"Welcome to the server, {member.mention} <3 \n {joke}")
@client.command(pass_context=True)
async def join(ctx):#allow to communicate with discord 
    if (ctx.author.vioce):
        channel=ctx.message.author.voice.channel
        await channel.connect()

    else:
        await ctx.send('you are not in a voice channel,sybau')

@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect
        await ctx.send("left the voice channel !!!")
    else:
        await ctx.send("you have to be in a voice channel in order to leave one")

#banning / unbanning users from the server

@client.command()
# @commmands.has_role()
@commands.has_any_role('moderator','Administrator','Owner')
async def ban(ctx,member:discord.Member,*,reason=None):
    # =ban member this user was being rude
    if reason == None:
        reason="THis user was banned by Aleeza"
    await member.ban(reason=reason)
#mkaing the option to kick users
@client.command()
@commands.has_any_role('moderator','Administrator','Owner')
async def kick(ctx,member:discord.Member,*,reason=None):
 
    if reason == None:
        reason="THis user was kicked by Aleeza"
    await member.kicl(reason=reason)
#mute users
@client.command()
@commands.has_any_role('moderator','Administrator','Owner')
        #=mute @username 100s

async def mute(ctx,member:discord.Member,timelimit):
    if 's' in timelimit:
        get_time=timelimit.strip('s')
        if get_time>2419000:
            await ctx.send('the time amount cannot be bigger than 28 days, you can always block them<3')

        else:    
           new_time=datetime.timedelta(seconds=int(get_time))
           await member.edit(timed_out_until=discord.utils.utcnow()+new_time)
    elif 'm'  in timelimit:  #minutes
        get_time=timelimit.strip('m')
        if get_time>40320:
            await ctx.send('the time amount cannot be bigger than 28 days, you can always block them<3')

        else:    
           new_time=datetime.timedelta(seconds=int(get_time))
           await member.edit(timed_out_until=discord.utils.utcnow()+new_time)

    elif 'd' in timelimit:
        get_time=timelimit.strip('d')
        if get_time>40320:
            await ctx.send('the time amount cannot be bigger than 28 days, you can always block them<3')

        else:    
           new_time=datetime.timedelta(seconds=int(get_time))
           await member.edit(timed_out_until=discord.utils.utcnow()+new_time)
    elif 'w' in timelimit:
           get_time=timelimit.strip('w')
           if get_time>4:
            await ctx.send('the time amount cannot be bigger than 28 days, you can always block them<3')

           else:    
             new_time=datetime.timedelta(seconds=int(get_time))
             await member.edit(timed_out_until=discord.utils.utcnow()+new_time)

#unmute users
@client.command()
@commands.has_any_role("Moderator,'Owner",'Administrator')
async def unmute(ctx,member:discord.Member):
    await member.edit(timed_out_until=None)
#making bot say a random ass joke

@client.command()
async def joke(ctx):
    """Fetches a random joke and sends it."""
    try:
        response = requests.get("https://v2.jokeapi.dev/joke/Any?type=single")
        data = response.json()
        joke = data.get("joke", "Hmm... I couldn't think of a joke right now ")
        await ctx.send(joke)
    except Exception as e:
        await ctx.send(f"Oops! Something went wrong: {e}")
@client.command()
async def ily(ctx):
    await ctx.send("I LOVE YOU TOO <3")

@client.command()
async def sybau(ctx):
    await ctx.send("GURT")
@client.command()
async def ping(ctx):
    await ctx.send('pong')

webserver.keep_alive()

#token
client.run(bottoken)






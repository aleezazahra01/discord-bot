import discord
import aiohttp
from discord.ext import commands
from datetime import datetime, timedelta
import webserver
import requests
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='=', intents=intents)

def mod_or_perms():
    async def predicate(ctx):
        roles = ['moderator', 'Administrator', 'Owner']
        if any(role.name in roles for role in ctx.author.roles):
            return True
        if ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.ban_members or ctx.author.guild_permissions.kick_members or ctx.author.guild_permissions.moderate_members:
            return True
        return False
    return commands.check(predicate)

@client.command()
@mod_or_perms()
async def helpme(ctx):
    embed = discord.Embed(
        title="Kuromi XD - Command List",
        description="Here are all my commands. Use `=` before each command!",
        color=discord.Color.purple()
    )
    embed.add_field(name="Moderation", value="""
    =ban @user reason - Ban a user
    =unban username#1234 - Unban a user
    =kick @user reason - Kick a user
    =mute @user time - Mute user for given time
    =unmute @user - Unmute a user
    """, inline=False)
    embed.add_field(name="Fun", value="""
    =hello - Say hello
    =bye - Say bye
    =sybau - OK XD
    =joke - Random lame ass joke
    =loveyou -Try It Yourself <3
    """, inline=False)
    embed.add_field(name="Voice", value="""
    =join
    =leave
    """, inline=False)
    await ctx.send(embed=embed)

@client.event
async def on_ready():
    print("The bot is ready for use")    # 
    print('--------------------------')

@client.command()
async def hello(ctx):
    await ctx.send("Hello, I'm Kuromi XD(a bitchy bot)")

@client.command()
async def bye(ctx):
    await ctx.send("Goodbye, have a good day <3")

@client.event
async def on_member_join(member):
    channel = client.get_channel(1404437300082905128)
    if not channel:
        return
    async with aiohttp.ClientSession() as session:
        async with session.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=explicit&type=single") as res:
            data = await res.json()
            joke = data.get("joke", "Couldn't fetch a joke")
    await channel.send(f"Welcome to the server, {member.mention} \n {joke}")

@client.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send('You are not in a voice channel')

@client.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel")
    else:
        await ctx.send("I'm not in a voice channel")
@client.command()
async def sybau():
    await ctx.send(" :( ")
@client.command():
async def loveyou():
    await ctx.send("I LOVE YOU TOO <3:) #so fucking unnecessary tho
@client.command()
@mod_or_perms()
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = "This user was banned"
    await member.ban(reason=reason)
    await ctx.send(f"{member} has been banned. Reason: {reason}")

@client.command()
@mod_or_perms()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    try:
        name, discriminator = member.split('#')
    except ValueError:
        await ctx.send("Please provide the username in this format: username#1234")
        return
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (name, discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user} has been unbanned")
            return
    await ctx.send("User not found in ban list.")

@client.command()
@mod_or_perms()
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = "This user was kicked by Admin"
    await member.kick(reason=reason)
    await ctx.send(f"{member} has been kicked. Reason: {reason}")

@client.command()
@mod_or_perms()
async def mute(ctx, member: discord.Member, timelimit):
    try:
        if timelimit.endswith("s"):
            duration = timedelta(seconds=int(timelimit[:-1]))
        elif timelimit.endswith("m"):
            duration = timedelta(minutes=int(timelimit[:-1]))
        elif timelimit.endswith("h"):
            duration = timedelta(hours=int(timelimit[:-1]))
        elif timelimit.endswith("d"):
            duration = timedelta(days=int(timelimit[:-1]))
        else:
            await ctx.send("Invalid time format ")
            return
        if duration.days > 28:
            await ctx.send("Mute duration cannot exceed 28 days.")
            return
        await member.edit(timed_out_until=discord.utils.utcnow() + duration)
        await ctx.send(f"{member} has been muted for {timelimit}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@client.command()
@mod_or_perms()
async def unmute(ctx, member: discord.Member):
    await member.edit(timed_out_until=None)
    await ctx.send(f"{member} has been unmuted")

@client.command()
async def joke(ctx):
    try:
        response = requests.get("https://v2.jokeapi.dev/joke/Any?type=single")
        data = response.json()
        joke = data.get("joke", "Couldn't think of a joke right now")
        await ctx.send(joke)
    except Exception as e:
        await ctx.send(f"Oops! Something went wrong")

@ban.error
@kick.error
@mute.error
@unmute.error
@unban.error
async def mod_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("OOPSIE You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument. Please check your command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid user or argument provided.")
    else:
        await ctx.send(f"An error occurred: {error}")

TOKEN = os.getenv("bottoken")

if __name__ == "__main__":
    webserver.keep_alive()
    client.run(TOKEN)  #your token goes here .

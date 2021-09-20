import discord
import os
from discord.ext import commands, tasks
import asyncio
import praw
import random
from praw import reddit
import youtube_dl
import pytube
import pathlib
import json
from pathlib import Path
from keep_alive import keep_alive

YTextract = pytube.extract

cwd = str(pathlib.Path.cwd())

my_secret = ""


reddit = ''
REDDIT_USER = ""
REDDIT_PASS = ""
REDDIT_ID = ""
REDDIT_SECRET = ""

def init():
    if os.environ.get('BOT_TOKEN') is not None:
        my_secret = os.environ['BOT_TOKEN']
    else:
        if os.path.exists("token.txt") == False:
            tok = open("token.txt","w")
            tok.write("")
            tok.close
            print("please put token in token.txt or add Evironment Variable called 'BOT_TOKEN' containing the token")
            exit()
        else:
            my_secret = open("token.txt","r")
            my_secret = my_secret.read()
    
    if os.path.exists("reddit_login.json") == False:
        reddit_login = {
            "REDDIT_USER":"",
            "REDDIT_PASS":"",
            "REDDIT_SECRET":"",
            "REDDIT_ID":"",}
        reddit_file = open("reddit_login.json","w")
        reddit_file.write(json.dumps(reddit_login,indent=4))
        reddit_file.close()
        print("check reddit_login.json")
    
    reddit_login = open("reddit_login.json","r")
    reddit_login = json.load(reddit_login)
    if os.environ.get('REDDIT_USER') is not None:
        REDDIT_USER = os.environ['REDDIT_USER']
        print("using env var")
    else:
        REDDIT_USER = reddit_login["REDDIT_USER"]
        print("using json")
    if os.environ.get('REDDIT_PASS') is not None:
        REDDIT_PASS = os.environ['REDDIT_PASS']
        print("using env var")
    else:
        REDDIT_PASS = reddit_login["REDDIT_PASS"]
        print("using json")
    if os.environ.get('REDDIT_ID') is not None:
        REDDIT_ID = os.environ['REDDIT_ID']
        print("using env var")
    else:
        REDDIT_ID = reddit_login["REDDIT_ID"]
        print("using json")
    if os.environ.get('REDDIT_SECRET') is not None:
        REDDIT_SECRET = os.environ['REDDIT_SECRET']
        print("using env var")
    else:
        REDDIT_SECRET = reddit_login["REDDIT_SECRET"]
        print("using json")
    reddit = praw.Reddit(client_id = REDDIT_ID,
                        client_secret = REDDIT_SECRET,
                        username = REDDIT_USER,
                        password = REDDIT_PASS,
                        user_agent = "UwU")
    if os.path.exists("./Audio/") == False:
        os.mkdir("./Audio")
    client.run(my_secret)

asyncio.get_event_loop().set_debug(True)

client = commands.Bot(command_prefix = "$")
client.remove_command("help")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#
# Error Handling
#
async def error_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You didnt give the arguments properly, try using help')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have manage_messages permssion')


#
#Messages
#
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('$what up'):
        await message.channel.send('All good How about you?')
    elif message.content.startswith('$can you do maths'):
        await message.channel.send('I hate maths bruh')
    elif message.content.startswith('$oke'):
        await message.channel.send('cool')
    elif message.content.startswith('$who created you'):
        await message.channel.send('Arya')
    elif message.content.startswith('$tell us about yourself'):
        await message.channel.send('I am a discord bot created by Arya using python on 14th september 2021')
    elif message.content.startswith('$rules'):
        await message.channel.send('I am too lazy to tell head over to #rules')
    elif message.content.startswith('$'):
         await client.process_commands(message)


#
#Errors
#


@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member,*, reason = "No reason provided"):
    try:
        await member.kick(reason = reason)
        await ctx.send(member.name + "was kicked, Because "+reason)
    except discord.errors.Forbidden:
        await ctx.send('I cant kick them :(.\nIm missing the permissions to kick them')


@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member,*, reason = "No reason provided"):
    try:
        await member.ban(reason = reason)
        await ctx.send(member.name + "was banned, Because "+reason)
    except discord.errors.Forbidden:
        await ctx.send('I cant ban them :(.\nIm missing the permissions to ban them')


@client.command(aliases=['m'])
@commands.has_permissions(kick_members = True)
async def mute(ctx, member : discord.Member,*, reason = "No reason provided"):
    await ctx.send(member.name + " was muted "+reason)
    Muted_role = ctx.guild.get_role(888628447851720704)
    await ctx.send(member.name + "was muted, Because "+reason)
    await member.add_roles(Muted_role)


@client.command(aliases=['um'])
@commands.has_permissions(kick_members = True)
async def unmute(ctx, member : discord.Member):
    Muted_role = ctx.guild.get_role(888628447851720704)
    await member.remove_roles(Muted_role)


@client.command(aliases=['user', 'info'])
@commands.has_permissions(kick_members = True)
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title = member.name, description = member.mention,  color = discord.Color.blue())
    embed.add_field(name = "ID", value = member.id, inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = "Requested by "+ ctx.author.name)
    await ctx.send(embed = embed)


@client.command()
async def meme(ctx):
    all_subs = []
    for submission in reddit.subreddit("memes").hot(limit=5):
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    em = discord.Embed(title = name)
    em.set_image(url = url)
    await ctx.send(embed = em)

@meme.error
async def error(ctx,error):
    if isinstance(error,discord.ext.commands.errors.CommandInvokeError):
        print("Please Check reddit_login.json and ensure that the login details are correct")



@client.command(aliases = ['join_vc'])
async def join(ctx):
    
    voiceChannel = ctx.author.voice.channel
    await voiceChannel.connect()


@client.command(name="p",aliases = ['play'])
async def p(ctx, url : str):
    filename = YTextract.video_id(url)
    song_there = False
    for obj in os.listdir('./Audio'):
        if obj == str(filename + ".opus"):
            song_there = True
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': './tmp.opus',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus',
        }],
    }
    if song_there == False:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".opus"):
                os.rename(file,filename + ".opus")
                os.replace(filename + ".opus",cwd + "/Audio/" + filename + ".opus")
    voice.play(discord.FFmpegPCMAudio("./Audio/" + filename + ".opus"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.group(invoke_without_command = True)
async def help(ctx):
    embed = discord.Embed(title = "help", desription = "Use $help <command> for extended info on a specific command.", color = ctx.author.color)
    embed.add_field(name = "Moderation", value = "Mute, Kick and Ban")
    embed.add_field(name = "Fun", value = "Memes")
    embed.add_field(name = "Info", value = "Info Card")
    await ctx.send(embed = embed)

@help.command()
async def kick(ctx):
    embed = discord.Embed(title = "Kick", description = "Kicks a member form the server", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "$kick <member> [reason]")
    await ctx.send(embed = embed)

@help.command()
async def ban(ctx):
    embed = discord.Embed(title = "Bans", description = "Bans a member form the server", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "$ban <member> [reason]")
    await ctx.send(embed = embed)

@help.command()
async def mute(ctx):
    embed = discord.Embed(title = "Mute", description = "Mutes a member", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "$mute <member> [reason]")
    await ctx.send(embed = embed)

@help.command()
async def memes(ctx):
    embed = discord.Embed(title = "Memes", description = "Send a meme from reddit", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "$meme")
    await ctx.send(embed = embed)

@help.command()
async def info(ctx):
    embed = discord.Embed(title = "Info", description = "sends a information card of a member", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "$whois <member>")
    await ctx.send(embed = embed)

keep_alive()
init()

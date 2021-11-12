from typing import Text
import discord
import os
from discord.ext import commands, tasks
import asyncio
import praw
import random
import youtube_dl
import pytube
import pathlib
import json
import pyyoutube

from praw import reddit
from pathlib import Path
from keep_alive import keep_alive

YTextract = pytube.extract
YTAPI = ""

cwd = str(pathlib.Path.cwd())

my_secret = ""

reddit = ''
REDDIT_USER = ""
REDDIT_PASS = ""
REDDIT_ID = ""
REDDIT_SECRET = ""

queue = []

prefix = "$"
ASCII_LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
ASCII_UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DECIMAL_DIGITS = "0123456789"
ALPHABETS = ASCII_LOWERCASE + ASCII_UPPERCASE

#reddit login code
if True:
    #checks if reddit_login exists
    if os.path.exists("login.json") == False:
        reddit_login = {
            "REDDIT_USER":"",
            "REDDIT_PASS":"",
            "REDDIT_SECRET":"",
            "REDDIT_ID":""}
        reddit_file = open("login.json","w")
        reddit_file.write(json.dumps(reddit_login,indent=4))
        reddit_file.close()
        print("check login.json")
    reddit_login = open("login.json","r")
    reddit_login = json.load(reddit_login)

    if os.path.exists("./Audio/") == False:
        os.mkdir("./Audio")
    
    if os.environ.get('LOGIN_BOT') is not None:
        reddit_login = json.loads(str(os.getenv('LOGIN_BOT')))
        print('using environment variables for reddit login')
    REDDIT_USER = reddit_login['REDDIT_USER']
    REDDIT_PASS = reddit_login['REDDIT_PASS']
    REDDIT_ID = reddit_login['REDDIT_ID']
    REDDIT_SECRET = reddit_login['REDDIT_SECRET']

    reddit = praw.Reddit(client_id = REDDIT_ID,
        client_secret = REDDIT_SECRET,
        username = REDDIT_USER,
        password = REDDIT_PASS,
        user_agent = "UwU",)
    

#^reddit login code

#Bot Login Code
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
    client.run(my_secret)
#^ Bot Login Code

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
async def on_message(ctx):
    if ctx.author == client.user:
        return

    elif ctx.content.startswith('$hello'):
        await ctx.channel.send('Hello!')
    elif ctx.content.startswith('$what up'):
        await ctx.channel.send('All good How about you?')
    elif ctx.content.startswith('$can you do maths'):
        await ctx.channel.send('I hate maths bruh')
    elif ctx.content.startswith('$oke'):
        await ctx.channel.send('cool')
    elif ctx.content.startswith('$who created you'):
        await ctx.channel.send('<@761976593194811392> and <@587606312825913366>')
    elif ctx.content.startswith('$tell us about yourself'):
        await ctx.channel.send('I am a discord bot created by Arya using python on 14th september 2021')
    elif ctx.content.startswith('$rules'):
        await ctx.channel.send('I am too lazy to tell head over to #rules')
    cprefix = check_prefix(ctx)
    client.command_prefix = str(cprefix)
    await client.process_commands(ctx)

#
## Reusable Commands
#

def get_conf(ctx,guild,prop):
  try:
    serverfile = open("Servers/" + str(ctx.guild.id)+ ".json","r")
    serverconfig = json.load(serverfile)
    val = serverconfig[str(prop)]
    return(val)
  except:
    return(None)

def get_user(ctx,guild,prop):
  try:
    serverfile = open("Users/" + str(ctx.guild.id)+ ".json","r")
    serverconfig = json.load(serverfile)
    val = serverconfig[str(prop)]
    return(val)
  except:
    return(None)

async def check_mod(ctx):
  modrole = get_conf(ctx,ctx.guild,'mod')
  if modrole is None:
    await ctx.send('This server doesnt have a configured MOD role!\n try using `' + check_prefix(ctx) + 'setup mod <name or id of mod role>')
    return(None)
  for i in ctx.author.roles:
    if i.id == modrole:
      return True
  return False

def check_prefix(ctx):
  cprefix = get_conf(ctx,ctx.guild,'prefix')
  c = list(str(cprefix))
  c = c[len(c) - 1]
  if cprefix != None:
    if c not in ALPHABETS:
      return(cprefix)
    else:
      return(str(cprefix + " "))
  else:
    return(prefix)

#
#Commands 
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
async def kiss(ctx):
    embed = discord.Embed(title = "this is a kiss")
    url = "https://c.tenor.com/3E9wNPpnltUAAAAM/zerotwo-anime.gif"
    embed.set_image(url = url)
    await ctx.send(embed = embed)

@client.command()
async def spank(ctx):
    embed = discord.Embed(title = "get spanked lol")
    url = "https://cdn.weeb.sh/images/By2iXyFw-.gif"
    embed.set_image(url = url)
    await ctx.send(embed = embed)

@client.command()
async def spank2(ctx):
    embed = discord.Embed(title = "get spanked lol")
    url = "https://cdn.weeb.sh/images/H1n57yYP-.gif"
    embed.set_image(url = url)
    await ctx.send(embed = embed)


@client.command()
async def meme(ctx,subreddit="memes"):
    all_subs = []
    for submission in reddit.subreddit(subreddit).top("day",limit=200):
        if submission.is_self == False:
            all_subs.append(submission)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    em = discord.Embed(title = name)
    em.set_image(url = url)
    await ctx.send(embed = em)

@client.command()
async def render(ctx):
    await meme(ctx,"blender")

@client.command()
async def bp(ctx):
    await meme(ctx,'BlackPink')

@client.command()
async def zerotwo(ctx):
    await meme(ctx,'ZeroTwo')

@client.command()
async def waifu(ctx):
    await meme(ctx,'Waifu')

@client.command()
async def kawai(ctx):
    await meme(ctx,'CuteAnimeGirls')

@client.command()
async def ab(ctx):
    await meme(ctx,'cuteanimeboys')
    

@meme.error
async def error(ctx,error):
    if isinstance(error,discord.ext.commands.errors.CommandInvokeError):
        print("Please Check reddit_login.json and ensure that the login details are correct")



@client.command(aliases = ['joinvc'])
async def join(ctx):
    voiceChannel = ctx.author.voice.channel
    await voiceChannel.connect()


@client.command(name="p",aliases = ['play'])
async def play(ctx, url : str):
    filename = YTextract.video_id(url)
    song_there = False
    video = pytube.YouTube(url=url)
    for obj in os.listdir('./Audio'):
        if obj == str(filename + ".opus"):
            song_there = True
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str('./' + filename + '.opus'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus',
        }],
    }
    if song_there == False:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            url = "https://youtube.com/watch?v=" + filename
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".opus"):
                os.rename(file,filename + ".opus")
                os.replace(filename + ".opus",cwd + "/Audio/" + filename + ".opus")
    try:
        await join(ctx)
    except:
        pass
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        voice.play(discord.FFmpegPCMAudio("./Audio/" + filename + ".opus"))
        print("playing: ",video.title)
        await ctx.send("playing: "+str(video.title))
    except discord.ext.commands.errors.CommandInvokeError:
        queue.append(url)




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
    embed = discord.Embed(title = "Help", desription = "Use $help <command> for extended info on a specific command.", color = ctx.author.color)
    embed.add_field(name = "Moderation", value = "Mute, Kick and Ban")
    embed.add_field(name = "Fun", value = "Memes")
    embed.add_field(name = "Info", value = "Info Card")
    embed.add_field(name = "chill", value = "Music")
    embed.add_field(name = "other", value = "Blakpink, ZeroTwo")
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
    embed = discord.Embed(title = "Memes", description = "Send a meme from memes subreddit", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "$meme")
    await ctx.send(embed = embed)

@help.command()
async def blackpink(ctx):
    embed = discord.Embed(title = "Blackpink", description = "Send a post from blackpink subreddit", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "$bp")
    await ctx.send(embed = embed)

@help.command()
async def ZeroTwo(ctx):
    embed = discord.Embed(title = "ZeroTwo", description = "Send a post from ZeroTwo subreddit", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "$zerotwo")
    await ctx.send(embed = embed)

@help.command()
async def info(ctx):
    embed = discord.Embed(title = "Info", description = "sends a information card of a member", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "$whois <member>")
    await ctx.send(embed = embed)

@help.command()
async def music(ctx):
    embed = discord.Embed(title = "music", description = "listen to music with your friends", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "$p <url>")
    await ctx.send(embed = embed)


@client.command(command="setup",help='setup the bot')
async def setup(ctx,prop=None,value=None):
  #only runs if the user is administrator
    if ctx.message.author.guild_permissions.administrator:
        if value:
            try:
                serverfile = open("Servers/" + str(ctx.message.guild.id)+  ".json","r")
            except:
                serverfile = open("Servers/" + str(ctx.message.guild.id)+ ".json","w")
            try:
                serverconfig = json.load(serverfile)
            except:
                serverconfig = {}
            print(serverconfig)
            if prop == "mod" or prop == "mute":
                checkrole1 = discord.utils.get(ctx.guild.roles, name = value)
                if checkrole1 == None:
                    checkrole1 = ctx.guild.get_role(int(value))
                if checkrole1 != None:
                    serverconfig[prop] = checkrole1.id
                    await ctx.send(prop + " is now " + str(checkrole1.name))
                else:
                    await ctx.send("That Role Doesnt Exist")
            else:
                serverconfig[str(prop)] = str(value)
                await ctx.send(str(prop)+" is now "+str(value))
                serverfile = open("servers/" + str(ctx.message.guild.id) + ".json","w")
                serverconfig = json.dump(serverconfig,serverfile,indent=4)
        else:
            await ctx.send("How to use:\nFirst of all after -setup you have to give it two arguements, one for the property and other for the properties value. for eg:\n-setup mod <name or id of mod role>\n for now these are the properties that have a meaning:\nmod\nprefix\nmute")
    else:
        await ctx.channel.send("get an admin to do this")



keep_alive()
init()

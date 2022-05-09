import discord
import youtube_dl
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

TOKEN = os.environ["TOKEN"]

#client = discord.Client()
client = commands.Bot(command_prefix='$')

players = {}

recently_played = []

#Print log on startup
@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


#on_message events listens for key messsages and returns response
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('ඞ!'):
    await message.channel.send('SUS!')

  if message.content.startswith('Noly'):
    await message.channel.send('', file=discord.File('./Assets/no_bitches.jpg'))

  await client.process_commands(message)

###########COMMANDS#########################################################
#echo command returns the string that was sent
@client.command()
async def echo(ctx, message):
    await ctx.send(message)

#ping command used to make sure bot is working properly
@client.command()
async def ping(ctx):
    await ctx.send('pong')

#bot will join the voice channel of the person who made the request 
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

#bot will leave current voice channel
@client.command(pass_context=True)
async def leave(ctx):
    await ctx.voice_client.disconnect()

#bot will play the audio of the youtube video that it sent via URL and add the url to recently played
@client.command()
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    recently_played.append(url)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
    else:
        await ctx.send("Already playing song")
        return

#bot will pause audio if it is playing
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice or voice.is_paused() or not voice.is_playing():
      await ctx.send("I'm not playing anything")
      return
    
    voice.pause()
    await ctx.send("Okay")
    

#bot will resume audio if it was paused
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice or not voice.is_connected():
      await ctx.send("I'm not in a call")
      return

    elif not voice.is_paused():
      await ctx.send("I'm not paused")
      return
    
    voice.resume()
    await ctx.send("Okay")



#bot will leave and join again, stoppig what is playing
@client.command(pass_context=True)
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice or not voice.is_connected():
      await ctx.send("I'm not in a call")
      return
    
    voice.stop()
    await ctx.send("Okay")
    return


#bot replays the last url entered into the recently_played array
@client.command(pass_content=True)
async def replay(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice or not voice.is_connected():
      await ctx.send("I'm not in a call")
      return
    elif not recently_played:
      await ctx.send("I haven't played anything yet")
      return
    elif voice.is_playing():
      await ctx.send("Already playing song")
      return
    elif voice.is_paused():
      await ctx.send("I am currently playing a song, it's just paused")
      return

    url = recently_played[len(recently_played)-1]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    recently_played.append(url)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
    else:
        await ctx.send("Already playing song")
        return


    return


#TEMP Prints a list of all URLS played during session. Needs to be revised bc there is a risk of spaming hundereds of urls.
@client.command(pass_content=True)
async def lop(ctx):
    i = 0
    for url in recently_played:
      i = i + 1

      str1 = str(i)
      str2 = ") "

      ret = str1+str2+url

      await ctx.send(ret)
    
    return



    
client.run(TOKEN)

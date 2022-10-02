#--SETUP(Viewonly)------------------------------------------------------------------
import os
import discord
from discord.ext import commands
from discord.utils import get
import ytm
from decouple import config
api = ytm.YouTubeMusic()
BTOKEN = config('TOKEN')
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='^', intents=intents)
def inList(toFind, List):
    if toFind in List:
        return
def clearConsole():
  command = 'clear'
  if os.name in('nt', 'dos'):
    command = 'cls'
  os.system(command)
#Main Code----------------------------------------------------------------------------
@bot.event
async def on_ready():
	clearConsole()
	print(f'Logged in ({bot.user})')
	await bot.change_presence(status=discord.Status.idle)

@bot.command(name='uwu', help='just dont.')
async def uwu(ctx):
  await ctx.send('*~uwu~*')

@bot.command(name='mute', help="Mute a person (Format: User, Mute dur, unit of time (S,M,H,D))")
@commands.has_permissions(administrator=True)
async def mute(ctx, person, time = -1, dur = 'N'):
	try:
		if time != -1 or dur != 'N':
			await ctx.send(f"User {person} has been muted for {time} seconds by {ctx.author}")
		else:
			await ctx.send(f"User {person} has been muted by {ctx.author}")
	except KeyboardInterrupt:
		return
	except Exception as e:
		await ctx.send(f"You have recieved an error: {e}")
#---Music Commands--------------------------------------------------------------------
musicPlaying = ""
musicQueue = []
@bot.command(name='playing', help='Will tell you what song is currently playing')
async def playing(ctx):
  await ctx.send(f"currently playing: {musicPlaying}")
@bot.command(name='play', help='Will queue a song and play it')
async def play(ctx, *arg):
	try:
		if len(arg) == 0:
			await ctx.send('Please enter a valid song')
			return
		argu = ''.join(arg)
		global musicPlaying
		global musicQueue
		channel = ctx.message.author.voice.channel
		voice = get(bot.voice_clients, guild=ctx.guild)
		if voice and voice.is_connected():
			await voice.move_to(channel)
		else:
			voice = await channel.connect()
		#suggestions = api.search_suggestions(arg)
		#suggestions[0]
		if musicQueue.__contains__(argu):
			await ctx.send('This song is already in queue')
		else:
			await ctx.send(f'Now Playing: {argu}')
		musicPlaying = argu
		if musicPlaying != "":
			if not musicQueue.__contains__(musicPlaying):
				musicQueue.append(musicPlaying)
	except KeyboardInterrupt:
		return
	except Exception as e:
		await ctx.send(f"You have recieved an error: {e}")
@bot.command(name='pause', help='Will pause the current song')
async def pause(ctx):
	try:
		global musicPlaying
		global musicQueue
		musicQueue.append(musicPlaying)
		musicPlaying = ""
		await ctx.send('Paused music')
	except KeyboardInterrupt:
		return
	except Exception as e:
		await ctx.send(f"You have recieved an error: {e}")
@bot.command(name='resume', help='Will resume the current song')
async def resume(ctx):
	try:
		global musicPlaying
		global musicQueue
		musicPlaying = musicQueue[musicQueue.__len__() - 1]
		del musicQueue[musicQueue.__len__() - 1]
		await ctx.send('Resuming music')
	except KeyboardInterrupt:
		return
	except Exception as e:
		await ctx.send(f"You have recieved an error: {e}")
@bot.command(name='skip', help='Will put the (next) song after all')
async def skip(ctx):
	try:
		global musicPlaying
		global musicQueue
		if musicPlaying == "":
			tempQueue = musicQueue[musicQueue.__len__() - 1]
			del musicQueue[musicQueue.__len__() - 1]
			musicQueue = [tempQueue, musicQueue]
		else:
			musicQueue = [musicPlaying, musicQueue]
			musicPlaying = ""
	except KeyboardInterrupt:
		return
	except Exception as e:
		await ctx.send(f"You have recieved an error: {e}")
@bot.command(name='queue', help='Will say the current song queue')
async def queue(ctx):
	try:
		global musicQueue
		await ctx.send(musicQueue)
	except KeyboardInterrupt:
		return
	except Exception as e:
		await ctx.send(f"You have recieved an error: {e}")
@bot.command(name='clearQueue', help='Will say the current song queue')
async def clearQueue(ctx):
	try:
		if ctx.author.guild_permissions.administrator:
			global musicQueue
			musicQueue.clear()
			await ctx.send('Queue cleared')
		else:
			await ctx.send('You do not have the proper permissions to perform this command')
	except KeyboardInterrupt:
		return
	except Exception as e:
		await ctx.send(f"You have recieved an error: {e}")
@bot.command(name='stop', help='Will stop the current song')
async def stop(ctx):
	try:
		global musicPlaying
		global musicQueue
		if musicPlaying != "":
			musicQueue.append(musicPlaying)
			musicPlaying = ""
		await ctx.send('Song stopped')
	except KeyboardInterrupt:
		return
	except Exception as e:
		await ctx.send(f"You have recieved an error: {e}")
@bot.command(name='bgSounds', help='Will play indoor lounge music')
async def bgSounds(ctx):
	try:
		channel = ctx.message.author.voice.channel
		voice = get(bot.voice_clients, guild=ctx.guild)
		if voice and voice.is_connected():
			await voice.move_to(channel)
		else:
			voice = await channel.connect()
			await ctx.send('Background Music Started')
	except KeyboardInterrupt:
		return
	except Exception as e:
		await ctx.send(f"You have recieved an error: {e}")
@bot.command(name='cut', help='Will no longer play sound')
async def cut(ctx):
	try:
		voice_client = ctx.message.guild.voice_client
		if voice_client.is_connected():
			await voice_client.disconnect()
		else:
			await ctx.send("The bot is not connected to a voice channel.")
	except KeyboardInterrupt:
		return
	except Exception as e:
		await ctx.send(f"You have recieved an error: {e}")
#Normal Chat------------------------------------------------------------------------
@bot.event
async def on_message(message):
	try:
		print(f'[{message.guild}, {message.author}] > {message.content}')
		if(message.author == bot.user):
			return
		if message.content.lower() == 'ping':
			await message.channel.send('Pong!')
		await bot.process_commands(message)
	except KeyboardInterrupt:
		return
	except Exception as e:
		await message.send(f"You have recieved an error: {e}")
#--LOGIN(Viewonly)------------------------------------------------------------------
bot.run(BTOKEN)
#EOF
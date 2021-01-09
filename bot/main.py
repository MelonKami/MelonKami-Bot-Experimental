#This is the experimental version of the bot!
import discord, datetime, json, codecs
from discord.ext import commands, tasks
from bot.utils import Config
from termcolor import colored
#from bot import utils
from os import path
#utils.Config

Config.hello_world()

#This need to stay on top of the code after the imports
print(colored('----STARTING DISCORD BOT----', 'green'))
startup_time = datetime.datetime.now()
print(startup_time.strftime("Time: %H:%M:%S"))
print()
#---------------------------------------

extensions_array = ["chat_commands"]

config = None
prefix = "!"



if path.exists('config.json') == False:
  print(colored("Hello, welcome to the bot's setup. To get started with the bot, you need to input your token and prefix", "green"))
  print()
  input_token = input("Token: ")
  input_prefix = input("Prefix: ")
  with open('config.json', 'x') as File:
      json.dump({"token": input_token, "prefix": input_prefix}, File, indent=4)

with codecs.open('config.json', 'r', encoding='utf-8-sig') as File:
    config = json.load(File)

def save_config():
    with codecs.open('config.json', 'w', encoding='utf8') as File:
        json.dump(config, File, sort_keys=True, indent=4, ensure_ascii=False)

def space(spaces):
  for x in range(spaces):
    print()

token = config["token"]

intents = discord.Intents.default()
bot = commands.Bot(
    command_prefix=prefix, case_insensitive=True, intents=intents)

@bot.command()
async def refresh(ctx):
  for extension in extensions_array:
    try:
      bot.reload_extension(extension)
    except:
      bot.load_extension(extension)

@bot.command()
async def extensions(ctx):
  await ctx.send("Extensions: \nchat_commands")
  for extension in extensions_array:
    await ctx.send(extension)

@bot.command()
async def unload_all_extensions(ctx):
  for extension in extensions_array:
    bot.unload_extension(extension)

@bot.command()
async def load_extension(ctx, extension):
  if extension in extensions_array:
    try:
      bot.load_extension(extension)
      await ctx.send("Extension has been successfully loaded")
    except:
      await ctx.send("This extension was already loaded")
  else:
    await ctx.send("This extension does not exist")

@bot.command()
async def unload_extension(ctx, extension):
  if extension in extensions_array:
    try:
      bot.unload_extension(extension)
      await ctx.send("Successfully unloaded extension")
    except:
      await ctx.send("Extension could either not be loaded, or something else went wrong")
  else:
    await ctx.send("This extension does not exist")

@tasks.loop(hours=1)
async def reload_extensions():
  for extension in extensions_array:
    try:
      bot.reload_extension(extension)
    except:
      bot.load_extension(extension)

@bot.event
async def on_ready():
    print(colored('----BOT HAS STARTED----', 'green'))
    bot_ready_time = datetime.datetime.now()
    print(bot_ready_time.strftime("Time: %H:%M:%S"))
    time = bot_ready_time - startup_time
    print(colored("Start up time:", "green"), colored(time, "red"))
    space(2)
    print('Logged in as {0.user}'.format(bot))
    print()
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Just a regular discord bot"))
    reload_extensions.start()

def run():
  bot.run(token)

#This is the experimental version of the bot!
import discord, datetime, json, os, codecs
from discord.ext import commands  #, tasks
from termcolor import colored
from os import path

#This need to stay on top of the code
print(colored('----STARTING DISCORD BOT----', 'green'))
startup_time = datetime.datetime.now()
print(startup_time.strftime("Time: %H:%M:%S"))
print()
#----------------------------------------

config = None
prefix = "!"

if path.exists('config.json') == False:
  if path.exists("first_config.json"):
    os.rename("first_config.json", "config.json")
  else:
    with open('config.json', 'x') as File:
        json.dump({}, File, indent=4)

with codecs.open('config.json', 'r', encoding='utf-8-sig') as File:
    config = json.load(File)

def save_config():
    with codecs.open('config.json', 'w', encoding='utf8') as File:
        json.dump(config, File, sort_keys=True, indent=4, ensure_ascii=False)

token = config["token"]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
    print(colored('----BOT HAS STARTED----', 'green'))
    bot_ready_time = datetime.datetime.now()
    print(bot_ready_time.strftime("Time: %H:%M:%S"))
    time = bot_ready_time - startup_time
    print(colored("Start up time took:", "green"), colored(time, "red"))
    print()
    print()
    print('Logged in as {0.user}'.format(bot))
    print()
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Jonas, I see what your doing"))

@bot.command()
async def ping(ctx):
    print("Command has been registered")
    await ctx.send("Din kommando has blitt registrert!")


bot.run(token)

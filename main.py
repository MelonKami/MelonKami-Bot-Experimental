#This is not the original version!
import discord, datetime
from discord.ext import commands  #, tasks
from termcolor import colored

print(colored('----STARTING DISCORD BOT----', 'green'))
startup_time = datetime.datetime.now()
print(startup_time.strftime("Time: %H:%M:%S"))
print()

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)


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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Jonas, I see what your doing"))

@bot.command()
async def ping(ctx):
    print("Command has been registered")
    await ctx.send("Din kommando has blitt registrert!")

bot.run('')

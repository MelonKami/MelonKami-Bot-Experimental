#Here are all the basic chat commads
from discord.ext import commands

print("Chat commands loaded")

class ChatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Command has been registered")

    @commands.command()
    async def test(self, ctx):
      await ctx.send("test")

def setup(bot):
    bot.add_cog(ChatCommands(bot))
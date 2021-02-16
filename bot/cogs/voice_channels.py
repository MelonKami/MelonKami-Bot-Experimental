from discord.ext import commands, tasks

class VoiceChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    #@commands.has_permissions(manage_messages=True)
    async def toggle_voice_chat(self, ctx):
        delete = False
        await ctx.send("Toggling voice chat")

        for category in ctx.guild.categories:
            if category.name == "Voice Chat Makers":
                delete = True
                await ctx.send("Deleting voice channels")
            if delete:
                if category.name == "Voice Chat Maker":
                    for channel in category.channels:
                        await channel.delete()
                if category.name == "Voice Chats":
                    for channel in category.channels:
                        await channel.delete()
            else:
                await ctx.send("Creating voice channels")
            

def setup(bot):
    bot.add_cog(VoiceChannel(bot))
from discord.ext import commands

class Events():
  def __init__(self):
    print('Event Cog loaded')

  @commands.Cog.listener()
  async def on_member_join(self, member):
    channel = member.guild.system_channel
    if channel is not None:
      await channel.send(f"Welcome {member.mention}")
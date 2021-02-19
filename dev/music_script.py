import discord, youtube_dl, datetime, asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio
from bot import utils    

ydl_opts = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'restrictfilenames': True,
    'noplaylist': True,
    'default_auto': 'auto'
}

def create_embed(title, description: str=None, url: str=None):
    embed = discord.Embed(title=title, description=description)
    embed.set_footer(text='Musikk! - ColosseumRP Bot')
    embed.url = url
    embed.timestamp = datetime.datetime.now()
    return embed

def format_number(number):
    value_pretty = f'{number:,}'
    return value_pretty.replace(',', ' ')

def source(song_info):
    print(song_info["title"])
    source = discord.PCMVolumeTransformer(
        discord.FFmpegPCMAudio(song_info["formats"][0]["url"], before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"),
        volume=1)
    return source       


def search(arg: str=None):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            get(arg)
        except:
            if arg == None:
                video = ydl.extract_info(f'ytsearch:music', download=False)['entries'][0]
            else:
                video = ydl.extract_info(f'ytsearch:{arg}', download=False)['entries'][0]
        else:
            video = ydl.extract_info(arg, download=False)
 
    return video

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def queue(self, ctx, *, song: str=None):
        index = 0
        if song == None:
            embed = create_embed(f'Dette er musikk køen', 'Her har du oversikt over sanger i kø for å spilles:')
            for sang in utils.config.config["musikk"]["kø"]:
                index += 1
                embed.add_field(name=index, value=sang)
            await ctx.send(embed=embed)
        else:
            song = search(song)
            await ctx.send(embed=create_embed(f'Lagt til i kø: **{song["title"]}**', f'Sang: __**{song["track"]}**__\n-Artist: **{song["artist"]}**\n-Varighet: {datetime.timedelta(seconds=song["duration"])}', url=song["url"]).set_image(url=song["thumbnail"]))
            utils.config.config["musikk"]["kø"].append(song["title"])
            utils.config.save_config()            
    
    @commands.command()
    async def skip(self, ctx):
        utils.config.config["musikk"]["skip"] = "True"
    
    @commands.command()
    async def stop(self, ctx):
        utils.config.config["musikk"]["stop"] = "True"
    
    @commands.command()
    async def play(self, ctx, *, link: str=None):
        if link == None:
            song_info = search()
        else:
            song_info = search(link)
        
        try:
            channel = ctx.message.author.voice.channel
            vc = await channel.connect()
            song_info = search(link)
            await ctx.send(embed=create_embed(f'Spiller nå: **{song_info["title"]}**', f'Sang: __**{song_info["track"]}**__\n-Artist: **{song_info["artist"]}**\n-Avspillinger: {format_number(int(song_info["view_count"]))}\n-Varighet: {datetime.timedelta(seconds=song_info["duration"])}', url=song_info["url"]).set_image(url=song_info["thumbnail"]))
            vc.play(source(song_info))
        except:
            await ctx.send('Det har oppstått en feil, mest sannsynlig så er allerede botten i en kanal, og spiller musikk, dersom dette er en feil, kontakt staff via !ticket')

        while vc.is_playing():
            await asyncio.sleep(1)
            while vc.is_playing():
                if utils.config.config["musikk"]["skip"] == "True":
                    utils.config.config["musikk"]["skip"] = "False"
                    if len(utils.config.config["musikk"]["kø"]) != 0:  
                        song = utils.config.config["musikk"]["kø"][0]
                        song_info = search(song)
                        await ctx.send(embed=create_embed(f'Skippet sang, spiller nå {song_info["title"]}', f'Sang: __**{song_info["track"]}**__\n-Artist: **{song_info["artist"]}**\n-Varighet: {datetime.timedelta(seconds=song_info["duration"])}', url=song_info["url"]).set_image(url=song_info["thumbnail"]))
                        vc.stop()
                        vc.play(source(search(song)))
                        utils.config.config["musikk"]["kø"].pop(0)
                        utils.config.save_config()
                    else:
                        await ctx.send('Det er ingen flere sanger i køen')
                elif utils.config.config["musikk"]["stop"] == "True":
                    utils.config.config["musikk"]["stop"] = "False"
                    vc.stop()
                    await vc.disconnect()
                    await ctx.send('Stopper musikken')

                await asyncio.sleep(1)
            else:
                await asyncio.sleep(5)


            if len(utils.config.config["musikk"]["kø"]) > 0:
                song = utils.config.config["musikk"]["kø"][0]
                song_info = search(song)
                await ctx.send(embed=create_embed(f'Spiller nå neste sang i køen: **{song_info["title"]}**', f'Sang: __**{song_info["track"]}**__\n-Artist: **{song_info["artist"]}**\n-Varighet: {datetime.timedelta(seconds=song_info["duration"])}', url=song_info["url"]).set_image(url=song_info["thumbnail"]))        
                vc.play(source(search(song)))
                utils.config.config["musikk"]["kø"].pop(0)
                utils.config.save_config()
            else:
                await ctx.send('Ingen flere sanger i kø, adjø')
                await vc.disconnect()
                utils.config.save_config()
                break

def setup(bot):
    bot.add_cog(Music(bot))
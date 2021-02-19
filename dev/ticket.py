import datetime, discord
from discord.ext import commands, tasks
from discord.utils import get
#from bot import utils

def create_embed(title, description: str=None, url: str=None):
    embed = discord.Embed(title=title, description=description)
    embed.set_footer(text='Ticket - ColosseumRP Bot')
    embed.url = url
    embed.timestamp = datetime.datetime.now()
    return embed

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Ticket cog has been loaded')

    @commands.command()
    async def ticket(self, ctx):
        await ctx.message.delete(delay=30)
        karakter = False
        utvikler = False
        tickets = 0
        tickets_array = []
        ticket_category = discord.utils.get(ctx.guild.categories, id=761690256139092052)
        admin = get(ctx.guild.roles, id=702955829891956736)
        moderator = get(ctx.guild.roles, id=703597644290850886)
        senior_admin = get(ctx.guild.roles, id=767202659044163584)
        utvikler = get(ctx.guild.roles, id=701884086545023097)
        
        moderator_pluss = [admin, moderator, senior_admin]
        administrator_pluss = [admin, senior_admin]
        senior_admin_pluss = [senior_admin]

        support_message = (f'Hallo {ctx.message.author.mention}, velkommen til Support! ' +
        'Ticketen blir automatisk arkivert 1 dag etter at siste melding har blitt sendt! ' +
        'Etter dette blir den lagret i opptil 30 dager, før den blir automatisk slettet igjen, vi kan lagre den lenger ' + 
        'om vi føler at det er nødvendig, men da vil du få en beskjed om det.')

        for channel in ticket_category.text_channels:
            if channel.name == f'ticket-{ctx.message.author.id}':
                tickets += 1
                tickets_array.append(channel)
            if tickets > 2:
                message_embed = create_embed('Åpne tickets', 'Vennligst referer til en av disse')

                for ticket in tickets_array:
                    message_embed.add_field(name='Åpen ticket', value=ticket.mention)
                message = await ctx.send(f'{ctx.message.author.mention}: Du har allerede 3 tickets åpne. Vennligst gjør deg ferdig med en av disse før du lager en ny en', embed=message_embed)
                await message.delete(delay=30)
                break
        else:
            ticket_create_overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.message.author: discord.PermissionOverwrite(read_messages=True, send_messages=False)
            }
            kanal = await ctx.guild.create_text_channel(f'ticket-{ctx.message.author.id}', overwrites=ticket_create_overwrites, category=ticket_category)
            def check(m):
                return m.channel == kanal and m.author.id == ctx.message.author.id
            def reaction_check(reaction, user):
                return user == ctx.message.author

            config_message = await kanal.send(embed=create_embed(f'Hallo {ctx.message.author.display_name}, velkommen til support', 'Vennligst trykk ' +
            'på tilsvarenede tall, etter hvilken staff rangering du trenger \n\n 1- Utvikler\n2-  Moderator\n3- Administrator\n4- Senior Administrator ' +
            '\n5- Eier'))
            message = await ctx.send(f'Din ticket ble laget {ctx.message.author.mention}!')
            await message.delete(delay=30)

            await config_message.add_reaction('1️⃣')
            await config_message.add_reaction('2️⃣')
            await config_message.add_reaction('3️⃣')
            await config_message.add_reaction('4️⃣')
            await config_message.add_reaction('5️⃣')

            reaction = await self.bot.wait_for('reaction_add', check=reaction_check)
            if '1' in str(reaction[0]):
                for role in ctx.guild.roles:
                    if role.name == 'Utvikler':
                        await kanal.set_permissions(role, read_messages=True, send_messages=True) 
                    if role in moderator_pluss:
                        await kanal.set_permissions(role, read_messages=True, send_messages=True)
            elif '2' in str(reaction[0]):
                for role in ctx.guild.roles:
                    if role in moderator_pluss:
                        await kanal.set_permissions(role, read_messages=True, send_messages=True)
            elif '3' in str(reaction[0]):
                for role in ctx.guild.roles:
                    if role in administrator_pluss:
                        await kanal.set_permissions(role, read_messages=True, send_messages=True)
            elif '4' in str(reaction[0]):
                for role in ctx.guild.roles:
                    if role in senior_admin_pluss:
                        await kanal.set_permissions(role, read_messages=True, send_messages=True)

            await config_message.delete()

            in_game = await kanal.send(embed=create_embed('Hva er problemet ditt relatert til?', '1- In-game\n2- UAK\n3- Utvikler'))
            
            await in_game.add_reaction('1️⃣')
            await in_game.add_reaction('2️⃣')
            await in_game.add_reaction('3️⃣')

            in_game_svar = await self.bot.wait_for('reaction_add', check=reaction_check)
            
            await kanal.set_permissions(ctx.message.author, read_messages=True, send_messages=True)

            if '1' in str(in_game_svar[0]):
                print('1')
                in_game_svar = 'In-game'

                karakter_navn_melding = await kanal.send(embed=create_embed('Ditt karakter navn', 'Hva er ditt karakter navn in-game?'))
                karakter_navn = await self.bot.wait_for('message', check=check)
                await karakter_navn.delete()
                await karakter_navn_melding.delete()
                karakter = True

            elif '2' in str(in_game_svar[0]):
                in_game_svar = 'UAK'
                print('2')
            elif '3' in str(in_game_svar[0]):
                in_game_svar = 'Utvikler'
                await kanal.set_permissions(utvikler, read_messages=True, send_messages=True)
            await in_game.delete()

            problem_melding = await kanal.send(embed=create_embed('Vennligst forklar ditt problem', 'For å gjøre tickets å effektivt og enkelt ' +
            'som mulig for oss, er det fint om du forklarer problemet ditt, så skal vi hjelpe deg så snart vi kan'))
            problem = await self.bot.wait_for('message', check=check)
            await problem.delete()

            await problem_melding.delete()
            if karakter:
                await kanal.send(embed=create_embed(f'Hei {ctx.message.author.display_name}, velkommen til support', f'{support_message} ' +
                f'\n\nKarakter Navn: {karakter_navn.content}' +
                f'\nUtvikler/In-game/UAK: {in_game_svar}\nProblem:\n{problem.content}'))
            else:
                await kanal.send(embed=create_embed(f'Hei {ctx.message.author.display_name}, velkommen til support', f'{support_message} ' +
                f'\n\nUtvikler/In-game/UAK: {in_game_svar}\nProblem:\n{problem.content}'))


def setup(bot):
    bot.add_cog(Ticket(bot))
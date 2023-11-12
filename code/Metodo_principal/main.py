import discord
from discord.ext import commands
import random
from decouple import config
import Apis as a

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
intents.members = True

SECRET_KEY = config("SECRET_KEY")

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print('Logado como {0}!'.format(bot.user))

@bot.hybrid_command()
async def teste(ctx, *args):
    await ctx.send(f'Olá, meu nome é {bot.user}, é um prazer {ctx.author}')

@bot.command(name= "r", help="Rola um dado de 20")
async def r(ctx, *args):
    if args[0] == '1d20':
        numero = random.randint(1, 20)
        if numero == 20:
            await ctx.send(f'Critou! O número é {numero}')
        else:
            await ctx.send(f'O número é {numero}')

@bot.command("moeda", help="Consulta de Cotação de uma moeda desejada !moeda <Sigla>")
async def moeda(ctx, *args):
    cotacao = a.Apis.CotacaoMoeda(args[0])
    await ctx.send(f'{cotacao}')

@bot.command(name="cep", help="Pesquisa de Cep no ViaCep !cep <cep>")
async def cep(ctx, *args):
    cep_escolhido = a.Apis.ConsultaCep(args[0])
    await ctx.send(f'{cep_escolhido}')

@bot.command(name="rastreio", help="Rastreio de Encomenda na base dos correios (Limite de 100 Requisições) !rastreio <código>")
async def rastreio(ctx, *args):
    mensagem = a.Apis.consulta_apicorreios(args[0])
    await ctx.send(f'{mensagem}')

bot.run(f'{SECRET_KEY}')

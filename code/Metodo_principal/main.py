from typing import Any, Optional, Type
import discord
from discord import app_commands
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

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(commands.when_mentioned_or('!'),intents=intents)
    
    async def setup_hook(self) -> None:
        await self.tree.sync()
    
bot = Bot()

@bot.event
async def on_ready():
    print('Logado como {0}!'.format(bot.user))

@bot.hybrid_command(name="ola",description="Envia uma saudação!",with_app_command=True)
async def runcommand(ctx: commands.context):
    await ctx.send(f'Olá, meu nome é {bot.user}, é um prazer {ctx.author}')

@bot.tree.command(name= "r",description="Rola um dado desejado ex: Dado de 20 <1d20>")
async def dado(Interaction: discord.Interaction, choice: str):
    if choice == '1d20':
        numero = random.randint(1, 20)
        if numero == 20:
            await Interaction.response.send_message(f'CRITOU! O número é {numero}')
        else: 
            await Interaction.response.send_message(f"O número é {numero}")
    else:
        await Interaction.response.send_message(f'Tipo de dado inválido')
#@bot.tree.command(name="teste",description="Teste")
#async def teste(Interaction: discord.Interaction,choice: str):
#        await Interaction.response.send_message(f"Teste {Interaction.user.mention} {choice}" )

@bot.tree.command(name="moeda", description="Consulta de Cotação de uma moeda desejada !moeda <Sigla>")
async def moeda(Interaction: discord.Interaction, choice: str):
    cotacao = a.Apis.CotacaoMoeda(choice)
    await Interaction.response.send_message(f'{Interaction.user.mention} \n{cotacao}')

@bot.tree.command(name="cep", description="Pesquisa de Cep no ViaCep !cep <cep>")
async def cep(Interaction: discord.Interaction, choice: str):
    cep_escolhido = a.Apis.ConsultaCep(choice)
    await Interaction.response.send_message(f'{Interaction.user.mention} \n{cep_escolhido}')

@bot.tree.command(name="rastreio", description="Rastreio de Encomenda na base dos correios (Limite de 100 Requisições) !rastreio <código>")
async def rastreio(Interaction: discord.Interaction, choice: str):
    mensagem = a.Apis.consulta_apicorreios(choice)
    await Interaction.response.send_message(f'{Interaction.user.mention} \n{mensagem}')

bot.run(f'{SECRET_KEY}')

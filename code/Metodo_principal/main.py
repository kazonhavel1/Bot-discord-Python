from typing import Any, Optional, Type
import discord
from discord import app_commands
from discord.ext import commands
import random
from decouple import config
import Apis as a
import yt_dlp as yt
import asyncio
import time


intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
intents.members = True
intents.voice_states = True

FFMPEG_OPTIONS = {
    'options': '-vn',
    'executable': 'FFMPEG/ffmpeg/bin/ffmpeg.exe'
}

YDL_OPTIONS = {'format' : 'bestaudio', 'noplaylist' : True}

SECRET_KEY = config("SECRET_KEY")

queue = []

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents)

    async def setup_hook(self) -> None:
        await self.tree.sync()

bot = Bot()



@bot.event
async def on_ready():
    print('Logado como {0}!'.format(bot.user))

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Comando digitado de forma incorreta, tente novamente.")
    print(error)

@bot.command()
async def playm(ctx, *, search):
    global musica_atual
    try:
        voice_ch = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_ch:
            return await ctx.send("Você não está em um canal de voz")

        if not ctx.voice_client:
            await voice_ch.connect()

        async with ctx.typing():
            with yt.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch: {search}",download=False)
                if "entries" not in info or len(info["entries"]) == 0:
                    return await ctx.send("Nenhum resultado encontrado.")
                video = info["entries"][0]
                url = video["url"]
                title = video["title"]
                queue.append((url,title))
                await ctx.send(f"Adicionado a fila: **{title}**")
                time.sleep(0.5)
            if not ctx.voice_client.is_playing():
                await play_next(ctx)
                return
    except Exception as e:
        await ctx.send(f"Erro ao efetuar o processo: {e}")
        return

async def play_next(ctx):
    global musica_atual
    if not ctx.voice_client.is_playing():
        if queue:
            url,title = queue.pop(0)
            musica_atual = title
            source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(
            source,
            after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop) if e is None else print(f"Erro na reprodução: {e}")
            )
            await ctx.send(f"Reproduzindo agora: **{title}**")
        else:
            await ctx.send ("A fila está vazia!")

@bot.command()
async def nextm(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Pulando para a próxima da fila.")
        time.sleep(0.5)
    else:
        await ctx.send("Não estou atualmente tocando algo.")

@bot.command()
async def filam(ctx):
    if queue:
        lista_formatada = "\n".join(f"{index + 1}. {nome}" for index, (_, nome) in enumerate(queue))
        await ctx.send(f"**Lista atual de Músicas**\n\nTocando Agora: **{musica_atual}**\n\nPróximas músicas:\n{lista_formatada}")
    else:
        await ctx.send("Lista de músicas vazia!")
    

@bot.command()
async def stopm(ctx):
    if ctx.voice_client:
        await ctx.send("Encerrando")
        await ctx.voice_client.disconnect()
    else:
       await ctx.send("Não estou em nenhum canal de voz neste momento.")

@bot.command()
async def gpt(ctx, *, texto: str = None):
    channel = ctx.channel.name

    if channel != "chat-bot":
        await ctx.send("Este comando só pode ser utilizado no canal 'chat-bot'. Caso não exista, solicite ao administrador sua criação e após tente novamente.")
        return

    async with ctx.typing():
        if texto:  # se o texto não está vazio
            retorno = a.Apis.geminiAi(f"{texto}")
            if len(retorno) > 2000:
                for i in range(0, len(retorno), 1990):
                    parte = retorno[i:i + 1990]
                    await ctx.send(f"Parte {i // 1990 + 1}:\n{parte}") # Caso o texto ultrapasse 2000 caracteres, o bot segrega em 2 ou mais mensagens
            else:
                await ctx.send(f"Olá {ctx.author.mention}, \n\n{retorno}")
                return
        else:
            await ctx.send("Erro ao efetuar o comando. Utilize-o assim: '!gpt Olá Gemini'")


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

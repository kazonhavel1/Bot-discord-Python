import discord
import random
from decouple import config
import requests

# Defina as intenções que o bot irá utilizar
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
intents.members = True

SECRET_KEY = config("SECRET_KEY")

class MyClient(discord.Client):    
    
    def CotacaoMoeda(moeda):
        #moeda = 'USD'
        cotacoes = requests.get(f"https://economia.awesomeapi.com.br/json/last/{moeda}-BRL")
        cotacoes = cotacoes.json()
        cotacaorecebida = float(cotacoes[f'{moeda}BRL']['bid'])
        return (f'A cotação da moeda {moeda} é R$ {round(cotacaorecebida,2)}.')
         
        
    async def on_ready(self):
        print('Logado como {0}!'.format(self.user))
        
    async def on_message(self,message):
        if message.content  == '!ola':
            await message.channel.send (f'Olá, meu nome é {self.user}, é um prazer {message.author}')
        elif message.content == '!r 1d20':
            numero = random.randint (1,20)
            while numero == 20:
                await message.channel.send (f'Critou! O número é {numero}')
                return
            else:
                await message.channel.send (f'O número é {numero}')      
        elif message.content == '!USD':
               cotacao = MyClient.CotacaoMoeda('USD')
               await message.channel.send (f'{cotacao}')
        elif message.content == '!EUR':
               cotacao = MyClient.CotacaoMoeda('EUR')
               await message.channel.send (f'{cotacao}')
        else:{
         print('Mensagem do autor {0.author}: {0.content}'.format(message))}
        
        
            
client = MyClient(intents=intents)  # Passa o objeto de intenções ao criar a instância do cliente
client.run(f'{SECRET_KEY}')  # TOKEN de acesso do BOT aqui

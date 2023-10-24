import discord
import random
from decouple import config
import Apis as a

# Defina as intenções que o bot irá utilizar
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
intents.members = True

SECRET_KEY = config("SECRET_KEY")

class MyClient(discord.Client):     
    
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
        elif '!moeda' in message.content:
               cotacao = a.Apis.CotacaoMoeda(message.content[7:14].replace(" ",""))
               await message.channel.send (f'{cotacao}')
        elif '!cep' in message.content:
                cepescolhido = a.Apis.ConsultaCep(message.content[5:13])
                await message.channel.send(f'{cepescolhido}')
        elif '!rastreio' in message.content:
                mensagem = a.Apis.consulta_apicorreios(message.content[10:24])
                await message.channel.send(f'{mensagem}')
        else:{
         print('Mensagem do autor {0.author}: {0.content}'.format(message))}
        
   
           
client = MyClient(intents=intents)  # Passa o objeto de intenções ao criar a instância do cliente
client.run(f'{SECRET_KEY}')  # TOKEN de acesso do BOT aqui


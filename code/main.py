import discord
import random
from decouple import config

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
        print(f'Variavel com o valor: {SECRET_KEY}')
        
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
        
        else:{
         print('Mensagem do autor {0.author}: {0.content}'.format(message))}
            
client = MyClient(intents=intents)  # Passa o objeto de intenções ao criar a instância do cliente
client.run(f'{SECRET_KEY}')  # TOKEN de acesso do BOT aqui

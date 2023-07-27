import discord
import random

# Defina as intenções que o bot irá utilizar
intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
intents.members = True

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logado como {0}!'.format(self.user))
        
    async def on_message(self,message):
        if message.content  == '!ola':
            await message.channel.send (f'Olá, meu nome é {self.user}, é um prazer {message.author}' )
        elif message.content == '!r 1d20':
            numero = random.randint (1,20)
            await message.channel.send (f'Saiu o número {numero}!')      
        else:{
         print('Mensagem do autor {0.author}: {0.content}'.format(message))}
            
client = MyClient(intents=intents)  # Passa o objeto de intenções ao criar a instância do cliente
client.run('MTEzMzkxMzc5NzIxMjUyMDQ3OA.GUtZeI.G1wA2TJ-FXxwXAPa6MXjTR-1VzjqUiO3WSsKTE') # TOKEN de acesso do BOT aqui

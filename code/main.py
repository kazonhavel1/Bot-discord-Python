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
        cotacoes = requests.get(f"https://economia.awesomeapi.com.br/json/last/{moeda}-BRL")
        cotacoes = cotacoes.json()
        if 'CoinNotExists' in str(cotacoes):
            return ('A moeda não foi encontrada ou não pode ser comparada :(')
        else:
            cotacaorecebida = float(cotacoes[f'{moeda}BRL']['bid'])
            nomemoeda = str(cotacoes[f'{moeda}BRL']['name'])
            return (f'A cotação da moeda {moeda} é R$ {round(cotacaorecebida,2)} ({nomemoeda}).')
         
    def ConsultaCep(cep):
        ceprecebido = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        ceprecebido = ceprecebido.json()

        if 'erro' in str(ceprecebido):
            return ('CEP não encontrado :(')
        else:
            retorno = ('CEP: ' + ceprecebido['cep'] + '\nLogradouro: ' + ceprecebido['logradouro'] + '\nBairro: '+ ceprecebido['bairro'] + '\nCidade: ' +
            ceprecebido['localidade'] + '\nEstado: ' + ceprecebido['uf'])
            return retorno
        

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
               cotacao = MyClient.CotacaoMoeda(message.content[7:14].replace(" ",""))
               await message.channel.send (f'{cotacao}')
        elif '!cep' in message.content:
                cepescolhido = MyClient.ConsultaCep(message.content[5:13])
                await message.channel.send(f'{cepescolhido}')
        else:{
         print('Mensagem do autor {0.author}: {0.content}'.format(message))}
        
        
            
client = MyClient(intents=intents)  # Passa o objeto de intenções ao criar a instância do cliente
client.run(f'{SECRET_KEY}')  # TOKEN de acesso do BOT aqui

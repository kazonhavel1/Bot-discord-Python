import json as j
import requests as r
from requests.structures import CaseInsensitiveDict
from decouple import config
from datetime import datetime as date

class Apis():
    
    def formata_datas(data):
        
        dataformatada = date.strptime(data,'%Y-%m-%dT%H:%M:%S')

        data_texto = dataformatada.strftime('%d/%m/%Y %H:%M:%S')

        return data_texto


    def rastreio_correiostxt(retorno):

        json = retorno

        dic = j.loads(json)

        objetos = dic['response']['objetos']

        objetos_formatados = objetos[0]

        eventos = objetos_formatados['eventos'] 

        ultimo_evento = dict(eventos[0])

        if dic["error"] == True:

            print(f'dic["message"]\nRequisições Restantes: {dic["api_limit_used"]}')

        else:

            try:
                penultimo_evento = eventos[1]
                if "RO" in penultimo_evento['codigo'] or "DO" in penultimo_evento['codigo']:
                    data_penevento = Apis.formata_datas(penultimo_evento['dtHrCriado'])
                    unidade_origem = f'{penultimo_evento["unidade"]["endereco"]["cidade"]} - {penultimo_evento["unidade"]["endereco"]["uf"]}'
                    unidade_destino = f'{penultimo_evento["unidadeDestino"]["endereco"]["cidade"]} - {penultimo_evento["unidadeDestino"]["endereco"]["uf"]}'
                    msg_penultimo_evento = f'\tDescrição do evento: {penultimo_evento["descricao"]}\n\tData do Evento: {data_penevento}\n\tUnidade Origem: {penultimo_evento["unidade"]["tipo"]} {unidade_origem}\n\tUnidade Destino: {penultimo_evento["unidade"]["tipo"]} {unidade_destino}'

                else:
                    data_penevento = Apis.formata_datas(penultimo_evento['dtHrCriado'])
                    unidade_origem = f'{penultimo_evento["unidade"]["endereco"]["cidade"]} - {penultimo_evento["unidade"]["endereco"]["uf"]}'
                    msg_penultimo_evento = f'\tDescrição do evento: {penultimo_evento["descricao"]}\n\tData do Evento: {data_penevento}\n\tUnidade: {penultimo_evento["unidade"]["tipo"]} {unidade_origem}'


            except:
                msg_penultimo_evento = '\tNenhum evento anterior ao Último'


            if "RO" in ultimo_evento['codigo'] or "DO" in ultimo_evento['codigo']:
                data_evento = Apis.formata_datas(ultimo_evento['dtHrCriado'])
                unidade_origem = f'{ultimo_evento["unidade"]["endereco"]["cidade"]} - {ultimo_evento["unidade"]["endereco"]["uf"]}'
                unidade_destino = f'{ultimo_evento["unidadeDestino"]["endereco"]["cidade"]} - {ultimo_evento["unidadeDestino"]["endereco"]["uf"]}'
                msg_ultimo_evento = f'\tDescrição do evento: {ultimo_evento["descricao"]}\nData do Evento: {data_evento}\nUnidade Origem: {ultimo_evento["unidade"]["tipo"]} {unidade_origem}\nUnidade Destino: {ultimo_evento["unidade"]["tipo"]} {unidade_destino}'
            else:
                data_evento = Apis.formata_datas(ultimo_evento['dtHrCriado'])
                unidade_origem = f'{ultimo_evento["unidade"]["endereco"]["cidade"]} - {ultimo_evento["unidade"]["endereco"]["uf"]}'
                msg_ultimo_evento = f'\tDescrição do evento: {ultimo_evento["descricao"]}\n\tData do Evento: {data_evento}\n\tUnidade: {ultimo_evento["unidade"]["tipo"]} {unidade_origem}'

        msg_final = f'\t\t\tSegue abaixo dados referente ao código {objetos_formatados["codObjeto"]}.\nÚltimo Evento:\n{msg_ultimo_evento}\n\nPenúltimo Evento:\n{msg_penultimo_evento}\n\n Requisições utilizadas (Limite 100): {dic["api_limit_used"]}'

        return msg_final



    def consulta_apicorreios(code):

        token = config("AuthAPICorreios")

        body = {
        "code": ''
        }
        body['code'] = code

        body_js = j.dumps(body)

        headers = CaseInsensitiveDict()
        
        
        headers['Content-Type'] = 'application/json'
        headers['SecretKey'] = '23f1c789-62ab-4650-af53-0612cc667088'
        headers['PublicToken'] =  '8IAZn7HKq7QJWbh37N3GOOeRVY'
        headers['DeviceToken'] = 'b08d732b-74f6-46cc-b52e-18947643dfbe'
        headers['Authorization'] = f'Bearer {token}'
        
        
        url = 'https://cluster.apigratis.com/api/v1/correios/rastreio'

        valor = r.post(url= url, data=body_js, headers=headers)
        valor = valor.text
  
        msg = Apis.rastreio_correiostxt(valor)
        
        return msg
    
    def CotacaoMoeda(moeda):
        cotacoes = r.requests.get(f"https://economia.awesomeapi.com.br/json/last/{moeda}-BRL")
        cotacoes = cotacoes.json()
        if 'CoinNotExists' in str(cotacoes):
            return ('A moeda não foi encontrada ou não pode ser comparada :(')
        else:
            cotacaorecebida = float(cotacoes[f'{moeda}BRL']['bid'])
            nomemoeda = str(cotacoes[f'{moeda}BRL']['name'])
            return (f'A cotação da moeda {moeda} é R$ {round(cotacaorecebida,2)} ({nomemoeda})., {cotacoes}')
         
    def ConsultaCep(cep):
        ceprecebido = r.requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        ceprecebido = ceprecebido.json()

        if 'erro' in str(ceprecebido):
            return ('CEP não encontrado :(')
        else:
            retorno = ('CEP: ' + ceprecebido['cep'] + '\nLogradouro: ' + ceprecebido['logradouro'] + '\nBairro: '+ ceprecebido['bairro'] + '\nCidade: ' +
            ceprecebido['localidade'] + '\nEstado: ' + ceprecebido['uf'])
            return retorno       

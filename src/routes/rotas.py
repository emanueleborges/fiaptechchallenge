"""
Módulo de rotas da API
"""
from flask import Blueprint, request, Response
import json

from src.services.servico_embrapa import ServicoEmbrapa
from src.controllers.controlador_producao import ControladorProducao
from src.config.configuracao import Configuracao

# Criar o blueprint da API
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/embrapa_data', methods=['GET'])
def obter_dados_producao():
    """
    Endpoint para obter os dados de produção da Embrapa
    
    Returns:
        Response: Objeto de resposta HTTP com dados em formato JSON
    """
    ano = request.args.get('ano', default=Configuracao.ANO_PADRAO, type=int)
    
    servico = ServicoEmbrapa()
    controlador = ControladorProducao()
    
    df_dados = servico.coletarDados(ano)
    resultado = controlador.formatarDados(df_dados)
    
    json_output = json.dumps(resultado, indent=4, ensure_ascii=False)
    return Response(json_output, mimetype='application/json')

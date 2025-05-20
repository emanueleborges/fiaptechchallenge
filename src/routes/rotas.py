"""
Módulo de rotas da API
"""
from flask import Blueprint, request, Response, jsonify
import json

from src.services.servico_embrapa import ServicoEmbrapa
from src.services.servico_processamento import ServicoProcessamento
from src.controllers.controlador_producao import ControladorProducao
from src.controllers.controlador_processamento import ControladorProcessamento
from src.config.configuracao import Configuracao

# Criar o blueprint da API
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificação de saúde da API
    
    Returns:
        Response: Objeto de resposta HTTP indicando o status da API
    """
    return jsonify({
        "status": "online",
        "message": "API de dados da Embrapa está funcionando corretamente"
    })

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

@api_blueprint.route('/embrapa_processamento', methods=['GET'])
def obter_dados_processamento():
    """
    Endpoint para obter os dados de processamento da Embrapa
    
    Returns:
        Response: Objeto de resposta HTTP com dados em formato JSON
    """
    ano = request.args.get('ano', default=Configuracao.ANO_PADRAO, type=int)
    formato = request.args.get('formato', default='padrao', type=str)
    opcao = request.args.get('opcao', default='opt_03', type=str)
    subopcao = request.args.get('subopcao', default=None, type=str)
    
    servico = ServicoProcessamento()
    controlador = ControladorProcessamento()
    
    df_dados = servico.coletarDadosProcessamento(ano, opcao=opcao, subopcao=subopcao)
    
    if formato.lower() == 'hierarquico':
        resultado = controlador.obterDadosHierarquicos(df_dados)
    else:
        resultado = controlador.formatarDados(df_dados)
    
    json_output = json.dumps(resultado, indent=4, ensure_ascii=False)
    return Response(json_output, mimetype='application/json')

"""
Módulo de rotas da API
"""
from flask import Blueprint, request, Response, jsonify
import json

from src.services.servico_embrapa import ServicoEmbrapa
from src.services.servico_processamento import ServicoProcessamento
from src.services.servico_comercializacao import ServicoComercializacao
from src.services.servico_importacao import ServicoImportacao
from src.services.servico_exportacao import ServicoExportacao
from src.controllers.controlador_producao import ControladorProducao
from src.controllers.controlador_processamento import ControladorProcessamento
from src.controllers.controlador_comercializacao import ControladorComercializacao
from src.controllers.controlador_importacao import ControladorImportacao
from src.controllers.controlador_exportacao import ControladorExportacao
from src.config.configuracao import Configuracao

# Constantes
MIME_TYPE_JSON = 'application/json'

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
def obter_dados_embrapa():
    """
    Endpoint unificado para obter os dados da Embrapa
    
    Query Parameters:
        ano: Ano para consulta (padrão: 2023)
        formato: Formato da resposta (padrão: 'padrao')
        opcao: Opção específica do relatório (opt_02 para produção, opt_03 para processamento, opt_04 para comercialização, opt_05 para importação, opt_06 para exportação)
        subopcao: Subopção específica do relatório (não utilizado para 'opt_02')
    
    Returns:
        Response: Objeto de resposta HTTP com dados em formato JSON
    """
    # Parâmetros comuns
    ano = request.args.get('ano', default=Configuracao.ANO_PADRAO, type=int)
    formato = request.args.get('formato', default='padrao', type=str).lower()
    
    # Obter opção da URL ou usar padrão de produção
    opcao = request.args.get('opcao', default=Configuracao.OPCAO_PRODUCAO, type=str)
      # Determinar a subopção padrão com base na opção
    subopcao_padrao = None
    if opcao == Configuracao.OPCAO_PROCESSAMENTO:
        subopcao_padrao = Configuracao.SUBOPCAO_PROCESSAMENTO_PADRAO
    elif opcao == Configuracao.OPCAO_IMPORTACAO:
        subopcao_padrao = Configuracao.SUBOPCAO_IMPORTACAO_PADRAO
    elif opcao == Configuracao.OPCAO_EXPORTACAO:
        subopcao_padrao = Configuracao.SUBOPCAO_EXPORTACAO_PADRAO
    
    subopcao = request.args.get('subopcao', default=subopcao_padrao, type=str)
    
    try:
        # Selecionar o serviço e controlador adequados com base na opção
        df_dados = None
        resultado = None
        
        if opcao == Configuracao.OPCAO_PRODUCAO:
            servico = ServicoEmbrapa()
            controlador = ControladorProducao()
            df_dados = servico.coletarDados(ano, opcao=opcao)
            resultado = controlador.formatarDados(df_dados)
            
        elif opcao == Configuracao.OPCAO_PROCESSAMENTO:
            servico = ServicoProcessamento()
            controlador = ControladorProcessamento()
            df_dados = servico.coletarDadosProcessamento(ano, opcao=opcao, subopcao=subopcao)
            
        elif opcao == Configuracao.OPCAO_COMERCIALIZACAO:
            servico = ServicoComercializacao()
            controlador = ControladorComercializacao()
            df_dados = servico.coletarDadosComercializacao(ano, opcao=opcao, subopcao=subopcao)
            
        elif opcao == Configuracao.OPCAO_IMPORTACAO:
            servico = ServicoImportacao()
            controlador = ControladorImportacao()
            df_dados = servico.coletarDadosImportacao(ano, opcao=opcao, subopcao=subopcao)
            
        elif opcao == Configuracao.OPCAO_EXPORTACAO:
            servico = ServicoExportacao()
            controlador = ControladorExportacao()
            df_dados = servico.coletarDadosExportacao(ano, opcao=opcao, subopcao=subopcao)
            
        else:
            return jsonify({
                "erro": f"Opção '{opcao}' não reconhecida",
                "opcoes_validas": [
                    Configuracao.OPCAO_PRODUCAO,
                    Configuracao.OPCAO_PROCESSAMENTO,
                    Configuracao.OPCAO_COMERCIALIZACAO, 
                    Configuracao.OPCAO_IMPORTACAO,
                    Configuracao.OPCAO_EXPORTACAO
                ]
            }), 400
          # Processar os dados conforme o formato para todos os tipos exceto produção
        if opcao != Configuracao.OPCAO_PRODUCAO and df_dados is not None:
            if formato.lower() == 'hierarquico':
                resultado = controlador.obterDadosHierarquicos(df_dados)
            else:
                resultado = controlador.formatarDados(df_dados)
        
        # Converter o resultado para JSON, independente da opção
        json_output = json.dumps(resultado, indent=4, ensure_ascii=False)
        return Response(json_output, mimetype=MIME_TYPE_JSON)
        
    except Exception as e:
        return jsonify({
            "erro": f"Erro ao processar dados: {str(e)}",
            "ano": ano,
            "opcao": opcao,
            "subopcao": subopcao
        }), 500

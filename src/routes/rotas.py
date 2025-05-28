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

MIME_TYPE_JSON = 'application/json'

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "message": "API de dados da Embrapa está funcionando corretamente!"
    })

@api_blueprint.route('/embrapa_data', methods=['GET'])
def obter_dados_embrapa():
    data = request.args.get('data', type=int)
    ano = request.args.get('ano', type=int) 
    
    if data is not None:
        ano_final = data
    elif ano is not None:
        ano_final = ano
    else:
        ano_final = Configuracao.ANO_PADRAO
    
    opcao = request.args.get('opcao', default=Configuracao.OPCAO_PRODUCAO, type=str)
    formato = request.args.get('formato', default='padrao', type=str).lower()
    
    subopcao_padrao = None
    if opcao == Configuracao.OPCAO_PROCESSAMENTO:
        subopcao_padrao = Configuracao.SUBOPCAO_PROCESSAMENTO_PADRAO
    elif opcao == Configuracao.OPCAO_IMPORTACAO:
        subopcao_padrao = Configuracao.SUBOPCAO_IMPORTACAO_PADRAO    
    elif opcao == Configuracao.OPCAO_EXPORTACAO:
        subopcao_padrao = Configuracao.SUBOPCAO_EXPORTACAO_PADRAO
    
    subopcao = request.args.get('subopcao', default=subopcao_padrao, type=str)
    
    try:
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
            print(f"Coletando dados de processamento: ano={ano}, opcao={opcao}, subopcao={subopcao}")
            df_dados = servico.coletarDadosProcessamento(ano, opcao=opcao, subopcao=subopcao)
            print(f"Dados coletados: {len(df_dados) if df_dados is not None else 'None'} registros")
            
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
                ]            }), 400
        
        if opcao != Configuracao.OPCAO_PRODUCAO and df_dados is not None:
            if formato.lower() == 'hierarquico':
                resultado = controlador.obterDadosHierarquicos(df_dados)
            else:
                resultado = controlador.formatarDados(df_dados)
        
        json_output = json.dumps(resultado, indent=4, ensure_ascii=False)
        return Response(json_output, mimetype=MIME_TYPE_JSON)
        
    except Exception as e:
        return jsonify({
            "erro": f"Erro ao processar dados: {str(e)}",
            "ano": ano,
            "opcao": opcao,
            "subopcao": subopcao
        }), 500

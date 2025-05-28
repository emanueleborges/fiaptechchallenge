import os

class Configuracao:
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    URL_BASE_EMBRAPA = os.getenv('EMBRAPA_BASE_URL', "http://vitibrasil.cnpuv.embrapa.br/index.php")
    
    API_EMBRAPA_DATA_URL = os.getenv('API_EMBRAPA_DATA_URL', '/embrapa_data?data={data}&opcao={opcao}')
    API_HEALTH_URL = os.getenv('API_HEALTH_URL', '/health')
    ANO_PADRAO = int(os.getenv('ANO_PADRAO', 2023))
    
    OPCAO_PRODUCAO = os.getenv('OPCAO_PRODUCAO', 'opt_02')
    OPCAO_PROCESSAMENTO = os.getenv('OPCAO_PROCESSAMENTO', 'opt_03')
    OPCAO_COMERCIALIZACAO = os.getenv('OPCAO_COMERCIALIZACAO', 'opt_04')
    OPCAO_IMPORTACAO = os.getenv('OPCAO_IMPORTACAO', 'opt_05')
    OPCAO_EXPORTACAO = os.getenv('OPCAO_EXPORTACAO', 'opt_06')
    
    SUBOPCAO_PROCESSAMENTO_PADRAO = os.getenv('SUBOPCAO_PROCESSAMENTO_PADRAO', 'subopt_03')
    SUBOPCAO_IMPORTACAO_PADRAO = os.getenv('SUBOPCAO_IMPORTACAO_PADRAO', 'subopt_03')
    SUBOPCAO_EXPORTACAO_PADRAO = os.getenv('SUBOPCAO_EXPORTACAO_PADRAO', 'subopt_03')
    
    PRODUTOS_IGNORADOS = os.getenv('PRODUTOS_IGNORADOS', 'Dados da Vitivinicultura,DOWNLOAD').split(',')
    PROCESSOS_IGNORADOS = os.getenv('PROCESSOS_IGNORADOS', 'Dados da Vitivinicultura,DOWNLOAD').split(',')
    PAISES_IGNORADOS = os.getenv('PAISES_IGNORADOS', 'Dados da Vitivinicultura,DOWNLOAD,Não consta na tabela').split(',')
    
    FORMATOS_RESPOSTA = os.getenv('FORMATOS_RESPOSTA', 'padrao,hierarquico').split(',')
    
    TIMEOUT = int(os.getenv('TIMEOUT', 120))
    WORKERS = int(os.getenv('WORKERS', 4))
    THREADS = int(os.getenv('THREADS', 2))

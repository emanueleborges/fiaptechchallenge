import os

class Configuracao:
    # Configurações do servidor
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
      # URLs da API
    URL_BASE_EMBRAPA = os.getenv('EMBRAPA_BASE_URL', "http://vitibrasil.cnpuv.embrapa.br/index.php")
    
    # URL padrão para todos os endpoints (apenas com parâmetros data e opcao)
    API_EMBRAPA_DATA_URL = os.getenv('API_EMBRAPA_DATA_URL', '/embrapa_data?data={data}&opcao={opcao}')
    API_HEALTH_URL = os.getenv('API_HEALTH_URL', '/health')
      # Configurações de dados
    ANO_PADRAO = int(os.getenv('ANO_PADRAO', 2023))
    
    # Opções da Embrapa (configuráveis via .env)
    OPCAO_PRODUCAO = os.getenv('OPCAO_PRODUCAO', 'opt_02')
    OPCAO_PROCESSAMENTO = os.getenv('OPCAO_PROCESSAMENTO', 'opt_03')
    OPCAO_COMERCIALIZACAO = os.getenv('OPCAO_COMERCIALIZACAO', 'opt_04')
    OPCAO_IMPORTACAO = os.getenv('OPCAO_IMPORTACAO', 'opt_05')
    OPCAO_EXPORTACAO = os.getenv('OPCAO_EXPORTACAO', 'opt_06')
    
    # Subopções padrão (configuráveis via .env)
    SUBOPCAO_PROCESSAMENTO_PADRAO = os.getenv('SUBOPCAO_PROCESSAMENTO_PADRAO', 'subopt_03')
    SUBOPCAO_IMPORTACAO_PADRAO = os.getenv('SUBOPCAO_IMPORTACAO_PADRAO', 'subopt_03')
    SUBOPCAO_EXPORTACAO_PADRAO = os.getenv('SUBOPCAO_EXPORTACAO_PADRAO', 'subopt_03')
    
    # Listas de itens ignorados (configuráveis via .env)
    PRODUTOS_IGNORADOS = os.getenv('PRODUTOS_IGNORADOS', 'Dados da Vitivinicultura,DOWNLOAD').split(',')
    PROCESSOS_IGNORADOS = os.getenv('PROCESSOS_IGNORADOS', 'Dados da Vitivinicultura,DOWNLOAD').split(',')
    PAISES_IGNORADOS = os.getenv('PAISES_IGNORADOS', 'Dados da Vitivinicultura,DOWNLOAD,Não consta na tabela').split(',')
    
    # Formatos de resposta suportados (configuráveis via .env)
    FORMATOS_RESPOSTA = os.getenv('FORMATOS_RESPOSTA', 'padrao,hierarquico').split(',')
    
    # Configurações adicionais
    TIMEOUT = int(os.getenv('TIMEOUT', 120))
    WORKERS = int(os.getenv('WORKERS', 4))
    THREADS = int(os.getenv('THREADS', 2))

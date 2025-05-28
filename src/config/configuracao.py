class Configuracao:
    URL_BASE_EMBRAPA = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    ANO_PADRAO = 2023
    OPCAO_PRODUCAO = "opt_02"
    OPCAO_PROCESSAMENTO = "opt_03"
    OPCAO_COMERCIALIZACAO = "opt_04"
    OPCAO_IMPORTACAO = "opt_05"
    OPCAO_EXPORTACAO = "opt_06"
    
    SUBOPCAO_PROCESSAMENTO_PADRAO = "subopt_03"
    SUBOPCAO_IMPORTACAO_PADRAO = "subopt_03"
    SUBOPCAO_EXPORTACAO_PADRAO = "subopt_03"
    
    PRODUTOS_IGNORADOS = ["Dados da Vitivinicultura", "DOWNLOAD"]
    
    PROCESSOS_IGNORADOS = ["Dados da Vitivinicultura", "DOWNLOAD"]
    
    PAISES_IGNORADOS = ["Dados da Vitivinicultura", "DOWNLOAD", "Não consta na tabela"]
    
    FORMATOS_RESPOSTA = ["padrao", "hierarquico"]

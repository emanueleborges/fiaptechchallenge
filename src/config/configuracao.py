"""
Configurações da aplicação.
"""

class Configuracao:
    """Classe que contém as configurações da aplicação."""
    
    # URL base para a API da Embrapa
    URL_BASE_EMBRAPA = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    
    # Ano padrão para consulta
    ANO_PADRAO = 2023
    
    # Opções de relatório
    OPCAO_PRODUCAO = "opt_02"
    OPCAO_PROCESSAMENTO = "opt_03"
    OPCAO_COMERCIALIZACAO = "opt_04"
    OPCAO_IMPORTACAO = "opt_05"
    OPCAO_EXPORTACAO = "opt_06"
    
    # Subopções de processamento
    SUBOPCAO_PROCESSAMENTO_PADRAO = "subopt_03"
    SUBOPCAO_IMPORTACAO_PADRAO = "subopt_03"
    SUBOPCAO_EXPORTACAO_PADRAO = "subopt_03"
    
    # Produtos que devem ser ignorados no processamento
    PRODUTOS_IGNORADOS = ["Dados da Vitivinicultura", "DOWNLOAD"]
    
    # Processos que devem ser ignorados no processamento
    PROCESSOS_IGNORADOS = ["Dados da Vitivinicultura", "DOWNLOAD"]
    
    # Países que devem ser ignorados na importação/exportação
    PAISES_IGNORADOS = ["Dados da Vitivinicultura", "DOWNLOAD", "Não consta na tabela"]
    
    # Formatos de resposta disponíveis
    FORMATOS_RESPOSTA = ["padrao", "hierarquico"]

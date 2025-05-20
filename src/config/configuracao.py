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
    
    # Subopções de processamento
    SUBOPCAO_PROCESSAMENTO_PADRAO = "subopt_03"
    
    # Produtos que devem ser ignorados no processamento
    PRODUTOS_IGNORADOS = ["Dados da Vitivinicultura", "DOWNLOAD"]
    
    # Processos que devem ser ignorados no processamento
    PROCESSOS_IGNORADOS = ["Dados da Vitivinicultura", "DOWNLOAD"]
    
    # Formatos de resposta disponíveis
    FORMATOS_RESPOSTA = ["padrao", "hierarquico"]

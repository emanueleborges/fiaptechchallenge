"""
Configurações da aplicação.
"""

class Configuracao:
    """Classe que contém as configurações da aplicação."""
    
    # URL base para a API da Embrapa
    URL_BASE_EMBRAPA = "http://vitibrasil.cnpuv.embrapa.br/index.php"
    
    # Ano padrão para consulta
    ANO_PADRAO = 2023
    
    # Produtos que devem ser ignorados no processamento
    PRODUTOS_IGNORADOS = ["Dados da Vitivinicultura", "DOWNLOAD"]
    
    # Processos que devem ser ignorados no processamento
    PROCESSOS_IGNORADOS = ["Dados da Vitivinicultura", "DOWNLOAD"]
    
    # Formatos de resposta disponíveis
    FORMATOS_RESPOSTA = ["padrao", "hierarquico"]

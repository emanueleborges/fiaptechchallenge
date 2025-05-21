"""
Controlador responsável pelo processamento dos dados de importação vinícola
"""
import pandas as pd
from typing import Dict, List, Any

from src.models.importacao import ModeloImportacao
from src.config.configuracao import Configuracao

class ControladorImportacao:
    def __init__(self):
        self.modelo = ModeloImportacao()
    
    def formatarDados(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        """
        Formata os dados do DataFrame para o formato desejado da API
        
        Args:
            df_dados: DataFrame com os dados de importação
            
        Returns:
            Dicionário formatado para ser convertido em JSON
        """
        # Estruturar os dados hierarquicamente
        resultado = {}
        quantidade_total = 0
        valor_total = 0.0
        
        # Extrair o total
        linha_total = df_dados[df_dados['pais'] == 'Total']
        if not linha_total.empty:
            quantidade_total = linha_total.iloc[0]['quantidade']
            valor_total = linha_total.iloc[0]['valor']
            # Remover o Total do DataFrame para processamento
            df_dados = df_dados[df_dados['pais'] != 'Total']
        
        # Processar os países (exceto os ignorados)
        paises = df_dados[~df_dados['pais'].isin(Configuracao.PAISES_IGNORADOS)]
        
        # Processar os países
        indice = 1
        for _, linha in paises.iterrows():
            nome_item = f"importacao {indice}"
            objeto_pais = {
                "pais": linha['pais'],
                "quantidade": linha['quantidade'],
                "valor": linha['valor']
            }
            resultado[nome_item] = objeto_pais
            indice += 1
        
        # Adicionar os totais ao resultado final
        resultado["total_quantidade"] = quantidade_total
        resultado["total_valor"] = valor_total
        
        return self.modelo.converterTiposNumpy(resultado)
    
    def obterDadosHierarquicos(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        """
        Organiza os dados em uma estrutura hierárquica de países.
        
        Args:
            df_dados: DataFrame com os dados de importação
            
        Returns:
            Dicionário com estrutura hierárquica dos dados
        """
        df_formatado = self.modelo.converterParaDataFrame(df_dados.to_dict('records'))
        hierarquia = self.modelo.estruturarHierarquia(df_formatado)
        
        # Adicionar os totais
        quantidade_total = 0
        valor_total = 0.0
        linha_total = df_dados[df_dados['pais'] == 'Total']
        if not linha_total.empty:
            quantidade_total = int(linha_total.iloc[0]['quantidade'])
            valor_total = float(linha_total.iloc[0]['valor'])
            
        resultado = {
            "paises": hierarquia,
            "totalGeral": {
                "quantidade": quantidade_total,
                "valor": valor_total
            }
        }
        
        return self.modelo.converterTiposNumpy(resultado)

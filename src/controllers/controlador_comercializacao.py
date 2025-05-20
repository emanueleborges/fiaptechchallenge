"""
Controlador responsável pelo processamento dos dados de comercialização vinícola
"""
import pandas as pd
from typing import Dict, List, Any

from src.models.comercializacao import ModeloComercializacao
from src.config.configuracao import Configuracao

class ControladorComercializacao:
    def __init__(self):
        self.modelo = ModeloComercializacao()
    
    def formatarDados(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        """
        Formata os dados do DataFrame para o formato desejado da API
        
        Args:
            df_dados: DataFrame com os dados de comercialização
            
        Returns:
            Dicionário formatado para ser convertido em JSON
        """
        # Estruturar os dados hierarquicamente
        resultado = {}
        total = 0
        
        # Extrair o total
        linha_total = df_dados[df_dados['produto'] == 'Total']
        if not linha_total.empty:
            total = linha_total.iloc[0]['quantidade']
            # Remover o Total do DataFrame para processamento
            df_dados = df_dados[df_dados['produto'] != 'Total']
        
        # Primeiro, processar os produtos pai (exceto os ignorados)
        produtos_pai = df_dados[(df_dados['ehPai']) & 
                              (~df_dados['produto'].isin(Configuracao.PRODUTOS_IGNORADOS))]
        
        produtos_dict = {}
        
        # Processar os produtos pai primeiro
        indice = 1
        for _, linha in produtos_pai.iterrows():
            nome_item = f"comercializacao {indice}"
            objeto_produto = {
                "produto": linha['produto'],
                "quantidade": linha['quantidade'],
                "destinos": []
            }
            resultado[nome_item] = objeto_produto
            produtos_dict[linha['produto']] = objeto_produto
            indice += 1
        
        # Processar os produtos filho
        produtos_filho = df_dados[(~df_dados['ehPai']) & 
                               (~df_dados['produto'].isin(Configuracao.PRODUTOS_IGNORADOS))]
        
        for _, linha in produtos_filho.iterrows():
            if linha['categoriaPai'] in produtos_dict:
                destino = {
                    "produto": linha['produto'],
                    "quantidade": linha['quantidade']
                }
                
                # Adicionar o destino se estiver disponível
                if 'destino' in linha and linha['destino']:
                    destino["destino"] = linha['destino']
                    
                produtos_dict[linha['categoriaPai']]["destinos"].append(destino)
        
        # Adicionar o total ao resultado final
        resultado["total"] = total
        
        return self.modelo.converterTiposNumpy(resultado)
    
    def obterDadosHierarquicos(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        """
        Organiza os dados em uma estrutura hierárquica de produtos e destinos.
        
        Args:
            df_dados: DataFrame com os dados de comercialização
            
        Returns:
            Dicionário com estrutura hierárquica dos dados
        """
        df_formatado = self.modelo.converterParaDataFrame(df_dados.to_dict('records'))
        hierarquia = self.modelo.estruturarHierarquia(df_formatado)
        
        # Adicionar o total
        total = 0
        linha_total = df_dados[df_dados['produto'] == 'Total']
        if not linha_total.empty:
            total = int(linha_total.iloc[0]['quantidade'])
            
        resultado = {
            "produtos": hierarquia,
            "totalGeral": total
        }
        
        return self.modelo.converterTiposNumpy(resultado)

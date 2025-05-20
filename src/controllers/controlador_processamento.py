"""
Controlador responsável pelo processamento dos dados de processamento vinícola
"""
import pandas as pd
from typing import Dict, List, Any

from src.models.processamento import ModeloProcessamento
from src.config.configuracao import Configuracao

class ControladorProcessamento:
    def __init__(self):
        self.modelo = ModeloProcessamento()
    
    def formatarDados(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        """
        Formata os dados do DataFrame para o formato desejado da API
        
        Args:
            df_dados: DataFrame com os dados de processamento
            
        Returns:
            Dicionário formatado para ser convertido em JSON
        """
        # Estruturar os dados hierarquicamente
        resultado = {}
        total = 0
        
        # Extrair o total
        linha_total = df_dados[df_dados['processo'] == 'Total']
        if not linha_total.empty:
            total = linha_total.iloc[0]['volume']
            # Remover o Total do DataFrame para processamento
            df_dados = df_dados[df_dados['processo'] != 'Total']
        
        # Primeiro, processar os processos pai (exceto os ignorados)
        processos_pai = df_dados[(df_dados['ehPai']) & 
                              (~df_dados['processo'].isin(Configuracao.PRODUTOS_IGNORADOS))]
        
        processos_dict = {}
        
        # Processar os processos pai primeiro
        indice = 1
        for _, linha in processos_pai.iterrows():
            nome_item = f"processo {indice}"
            objeto_processo = {
                "processo": linha['processo'],
                "volume": linha['volume'],
                "subprocessos": []
            }
            resultado[nome_item] = objeto_processo
            processos_dict[linha['processo']] = objeto_processo
            indice += 1
        
        # Processar os processos filho
        processos_filho = df_dados[(~df_dados['ehPai']) & 
                                (~df_dados['processo'].isin(Configuracao.PRODUTOS_IGNORADOS))]
        
        for _, linha in processos_filho.iterrows():
            if linha['categoriaPai'] in processos_dict:
                subprocesso = {
                    "processo": linha['processo'],
                    "volume": linha['volume']
                }
                
                # Adicionar o método se estiver disponível
                if 'metodo' in linha and linha['metodo']:
                    subprocesso["metodo"] = linha['metodo']
                    
                processos_dict[linha['categoriaPai']]["subprocessos"].append(subprocesso)
        
        # Adicionar o total ao resultado final
        resultado["total"] = total
        
        return self.modelo.converterTiposNumpy(resultado)
    
    def obterDadosHierarquicos(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        """
        Organiza os dados em uma estrutura hierárquica de processos e subprocessos.
        
        Args:
            df_dados: DataFrame com os dados de processamento
            
        Returns:
            Dicionário com estrutura hierárquica dos dados
        """
        df_formatado = self.modelo.converterParaDataFrame(df_dados.to_dict('records'))
        hierarquia = self.modelo.estruturarHierarquia(df_formatado)
        
        # Adicionar o total
        total = 0
        linha_total = df_dados[df_dados['processo'] == 'Total']
        if not linha_total.empty:
            total = int(linha_total.iloc[0]['volume'])
            
        resultado = {
            "processos": hierarquia,
            "totalGeral": total
        }
        
        return self.modelo.converterTiposNumpy(resultado)

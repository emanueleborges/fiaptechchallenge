"""
Controlador responsável pelo processamento dos dados de processamento vinícola
"""
import pandas as pd
from typing import Dict, Any, List

from src.models.processamento import ModeloProcessamento
from src.config.configuracao import Configuracao

class ControladorProcessamento:
    def __init__(self):
        self.modelo = ModeloProcessamento()
    
    def formatarDados(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        """
        Formata os dados do DataFrame para o formato desejado da API:
        {
          "Total": <int>,
          "itens": [
            {
              "produto": <str>,
              "quantidade": <int>,
              "subitem": [
                { "produto": <str>, "quantidade": <int> },
                ...
              ]
            },
            ...
          ]
        }
        """
        # Cópia para não alterar o DataFrame original
        df = df_dados.copy()

        # Extrair e remover o Total
        linha_total = df[df['processo'] == 'Total']
        total = int(linha_total.iloc[0]['volume']) if not linha_total.empty else 0
        df = df[df['processo'] != 'Total']

        # Identificar pais e filhos (ignorando itens conforme Configuracao)
        pais = df[
            (df['ehPai']) &
            (~df['processo'].isin(Configuracao.PRODUTOS_IGNORADOS))
        ]
        filhos = df[
            (~df['ehPai']) &
            (~df['processo'].isin(Configuracao.PRODUTOS_IGNORADOS))
        ]

        itens: List[Dict[str, Any]] = []
        for _, pai in pais.iterrows():
            nome_pai = pai['processo']
            quantidade_pai = pai['volume']

            # Monta lista de subitens
            subitems: List[Dict[str, Any]] = []
            df_filhos = filhos[filhos['categoriaPai'] == nome_pai]
            for _, filho in df_filhos.iterrows():
                subitems.append({
                    "produto": filho['processo'],
                    "quantidade": int(filho['volume'])
                })

            itens.append({
                "produto": nome_pai,
                "quantidade": int(quantidade_pai),
                "subitem": subitems
            })

        # Monta objeto final
        resultado = {
            "Total": total,
            "itens": itens
        }

        # Converte tipos NumPy para nativos antes de retornar
        return self.modelo.converterTiposNumpy(resultado)
    
    def obterDadosHierarquicos(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        """
        Organiza os dados em uma estrutura hierárquica de processos e subprocessos.
        """
        df_formatado = self.modelo.converterParaDataFrame(df_dados.to_dict('records'))
        hierarquia = self.modelo.estruturarHierarquia(df_formatado)
        
        # Extrair Total novamente
        linha_total = df_dados[df_dados['processo'] == 'Total']
        total = int(linha_total.iloc[0]['volume']) if not linha_total.empty else 0
        
        resultado = {
            "processos": hierarquia,
            "totalGeral": total
        }
        
        return self.modelo.converterTiposNumpy(resultado)

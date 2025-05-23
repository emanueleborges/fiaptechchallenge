"""
Controlador responsável pelo processamento dos dados de importação vinícola
"""
import pandas as pd
from typing import Dict, Any, List

from src.models.importacao import ModeloImportacao
from src.config.configuracao import Configuracao

class ControladorImportacao:
    def __init__(self):
        self.modelo = ModeloImportacao()
    
    def formatarDados(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        """
        Formata os dados do DataFrame para o formato desejado da API:
        {
          "Total": <int>,              # soma das quantidades
          "itens": [
            {
              "produto": <str>,        # país de origem
              "quantidade": <int>,     # volume importado
              "valor": <float>,        # valor da importação
              "subitem": []            # sempre vazio para importação
            },
            ...
          ]
        }
        """
        # Cópia para não alterar o DataFrame original
        df = df_dados.copy()

        # Extrair e remover o Total
        linha_total = df[df['pais'] == 'Total']
        total = int(linha_total.iloc[0]['quantidade']) if not linha_total.empty else 0
        df = df[df['pais'] != 'Total']

        # Construir lista de itens
        itens: List[Dict[str, Any]] = []
        for _, row in df.iterrows():
            pais = row['pais']
            if pais in Configuracao.PAISES_IGNORADOS:
                continue
            itens.append({
                "produto": pais,
                "quantidade": int(row['quantidade']),
                "valor": float(row['valor']),
                "subitem": []
            })

        # Montar objeto final
        resultado = {
            "Total": total,
            "itens": itens
        }

        # Converter tipos NumPy para nativos antes de retornar
        return self.modelo.converterTiposNumpy(resultado)
    
    def obterDadosHierarquicos(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        """
        Organiza os dados em uma estrutura hierárquica de países.
        """
        df_formatado = self.modelo.converterParaDataFrame(df_dados.to_dict('records'))
        hierarquia = self.modelo.estruturarHierarquia(df_formatado)
        
        # Extrair Total de quantidade
        linha_total = df_dados[df_dados['pais'] == 'Total']
        total = int(linha_total.iloc[0]['quantidade']) if not linha_total.empty else 0
        
        resultado = {
            "produtos": hierarquia,
            "totalGeral": total
        }
        
        return self.modelo.converterTiposNumpy(resultado)

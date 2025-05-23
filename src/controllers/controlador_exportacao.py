"""
Controlador responsável pelo processamento dos dados de exportação vinícola
"""
import pandas as pd
from typing import Dict, Any, List

from src.models.exportacao import ModeloExportacao
from src.config.configuracao import Configuracao

class ControladorExportacao:
    def __init__(self):
        self.modelo = ModeloExportacao()
    
    def formatarDados(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        """
        Formata os dados do DataFrame para o formato desejado da API:
        {
          "Total": <int>,              # soma das quantidades exportadas
          "itens": [
            {
              "produto": <str>,        # país de destino
              "quantidade": <int>,     # volume exportado
              "valor": <float>,        # valor da exportação
              "subitem": []            # sempre vazio nesta visão
            },
            ...
          ]
        }
        """
        # Cópia para não alterar o DataFrame original
        df = df_dados.copy()

        # Extrair e remover o Total
        linha_total = df[df['pais'] == 'Total']
        total_quantidade = int(linha_total.iloc[0]['quantidade']) if not linha_total.empty else 0
        df = df[df['pais'] != 'Total']

        # Construir lista de itens (cada país é um "produto")
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
            "Total": total_quantidade,
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
        
        # Extrair Total novamente
        linha_total = df_dados[df_dados['pais'] == 'Total']
        total_quantidade = int(linha_total.iloc[0]['quantidade']) if not linha_total.empty else 0
        
        resultado = {
            "produtos": hierarquia,
            "totalGeral": total_quantidade
        }
        
        return self.modelo.converterTiposNumpy(resultado)

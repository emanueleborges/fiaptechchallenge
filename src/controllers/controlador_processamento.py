import pandas as pd
from typing import Dict, Any, List

from src.models.processamento import ModeloProcessamento
from src.config.configuracao import Configuracao

class ControladorProcessamento:
    def __init__(self):
        self.modelo = ModeloProcessamento()
    
    def formatarDados(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        df = df_dados.copy()

        linha_total = df[df['processo'] == 'Total']
        total = int(linha_total.iloc[0]['volume']) if not linha_total.empty else 0
        df = df[df['processo'] != 'Total']

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

        resultado = {
            "Total": total,
            "itens": itens
        }

        return self.modelo.converterTiposNumpy(resultado)
    
    def obterDadosHierarquicos(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        df_formatado = self.modelo.converterParaDataFrame(df_dados.to_dict('records'))
        hierarquia = self.modelo.estruturarHierarquia(df_formatado)
        
        linha_total = df_dados[df_dados['processo'] == 'Total']
        total = int(linha_total.iloc[0]['volume']) if not linha_total.empty else 0
        
        resultado = {
            "processos": hierarquia,
            "totalGeral": total
        }
        
        return self.modelo.converterTiposNumpy(resultado)

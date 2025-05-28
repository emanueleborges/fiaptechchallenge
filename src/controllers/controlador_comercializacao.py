import pandas as pd
from typing import Dict, Any, List

from src.models.comercializacao import ModeloComercializacao
from src.config.configuracao import Configuracao

class ControladorComercializacao:
    def __init__(self):
        self.modelo = ModeloComercializacao()
    
    def formatarDados(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        df = df_dados.copy()

        linha_total = df[df['produto'] == 'Total']
        total = int(linha_total.iloc[0]['quantidade']) if not linha_total.empty else 0
        df = df[df['produto'] != 'Total']

        pais = df[
            (df['ehPai']) &
            (~df['produto'].isin(Configuracao.PRODUTOS_IGNORADOS))
        ]
        filhos = df[
            (~df['ehPai']) &
            (~df['produto'].isin(Configuracao.PRODUTOS_IGNORADOS))
        ]

        itens: List[Dict[str, Any]] = []
        for _, pai in pais.iterrows():
            nome_pai = pai['produto']
            quantidade_pai = pai['quantidade']

            subitems: List[Dict[str, Any]] = []
            df_filhos = filhos[filhos['categoriaPai'] == nome_pai]
            for _, filho in df_filhos.iterrows():
                subitems.append({
                    "produto": filho['produto'],
                    "quantidade": int(filho['quantidade'])
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
        
        linha_total = df_dados[df_dados['produto'] == 'Total']
        total = int(linha_total.iloc[0]['quantidade']) if not linha_total.empty else 0
        
        resultado = {
            "produtos": hierarquia,
            "totalGeral": total
        }
        
        return self.modelo.converterTiposNumpy(resultado)

"""
Controlador responsável pelo processamento dos dados de produção
"""
import pandas as pd
from typing import Dict, List, Any

from src.models.producao import ModeloProducao
from src.config.configuracao import Configuracao

class ControladorProducao:
    def __init__(self):
        self.modelo = ModeloProducao()
        
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
        # Cópia para não alterar o df original
        df = df_dados.copy()

        # Extrair e remover Total
        linha_total = df[df['Produto'] == 'Total']
        total = int(linha_total.iloc[0]['Quantidade (L.)']) if not linha_total.empty else 0
        df = df[df['Produto'] != 'Total']

        # Filtrar produtos pai
        pais = df[
            (df['is_parent']) &
            (~df['Produto'].isin(Configuracao.PRODUTOS_IGNORADOS))
        ]

        # Filtrar produtos filhos
        filhos = df[~df['is_parent']]

        itens = []
        for _, pai in pais.iterrows():
            nome_pai = pai['Produto']
            quantidade_pai = pai['Quantidade (L.)']

            # Encontrar todos os filhos deste pai
            subitems = []
            df_filhos = filhos[filhos['Categoria_Pai'] == nome_pai]
            for _, filho in df_filhos.iterrows():
                subitems.append({
                    "produto": filho['Produto'],
                    "quantidade": int(filho['Quantidade (L.)'])
                })

            itens.append({
                "produto": nome_pai,
                "quantidade": int(quantidade_pai),
                "subitem": subitems
            })

        # Montar estrutura final
        resultado = {
            "Total": total,
            "itens": itens
        }

        # Converter tipos numpy (se necessário)
        return self.modelo.converterTiposNumpy(resultado)

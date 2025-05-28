import pandas as pd
from typing import Dict, Any, List

from src.models.importacao import ModeloImportacao
from src.config.configuracao import Configuracao

class ControladorImportacao:
    def __init__(self):
        self.modelo = ModeloImportacao()
    
    def formatarDados(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        df = df_dados.copy()
        linha_total = df[df['pais'] == 'Total']
        total = int(linha_total.iloc[0]['quantidade']) if not linha_total.empty else 0
        df = df[df['pais'] != 'Total']
        
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

        resultado = {
            "Total": total,
            "itens": itens
        }
        
        return self.modelo.converterTiposNumpy(resultado)
    
    def obterDadosHierarquicos(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        df_formatado = self.modelo.converterParaDataFrame(df_dados.to_dict('records'))
        hierarquia = self.modelo.estruturarHierarquia(df_formatado)
        
        linha_total = df_dados[df_dados['pais'] == 'Total']
        total = int(linha_total.iloc[0]['quantidade']) if not linha_total.empty else 0
        
        resultado = {
            "paises": hierarquia,
            "totalGeral": total
        }
        
        return self.modelo.converterTiposNumpy(resultado)

import pandas as pd
from typing import Dict, Any, List

from src.models.exportacao import ModeloExportacao
from src.config.configuracao import Configuracao

class ControladorExportacao:
    def __init__(self):
        self.modelo = ModeloExportacao()
    
    def formatarDados(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        df = df_dados.copy()

        linha_total = df[df['pais'] == 'Total']
        total_volume = int(linha_total.iloc[0]['volume']) if not linha_total.empty else 0
        total_valor = float(linha_total.iloc[0]['valor']) if not linha_total.empty else 0.0
        
        df = df[df['pais'] != 'Total']
        df = df[~df['pais'].isin(Configuracao.PAISES_IGNORADOS)]
        
        itens: List[Dict[str, Any]] = []
        for _, linha in df.iterrows():
            pais = linha['pais']
            volume = int(linha['volume'])
            valor = float(linha['valor'])
            
            itens.append({
                "produto": pais,
                "quantidade": volume,
                "valor": valor,
                "subitem": []
            })
        
        resultado = {
            "Total": total_volume,
            "TotalValor": total_valor,
            "itens": itens
        }
        
        return self.modelo.converterTiposNumpy(resultado)
    
    def obterDadosHierarquicos(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        df_formatado = self.modelo.converterParaDataFrame(df_dados.to_dict('records'))
        hierarquia = self.modelo.estruturarHierarquia(df_formatado)
        
        linha_total = df_dados[df_dados['pais'] == 'Total']
        total_volume = int(linha_total.iloc[0]['volume']) if not linha_total.empty else 0
        total_valor = float(linha_total.iloc[0]['valor']) if not linha_total.empty else 0.0
        
        resultado = {
            "paises": hierarquia,
            "totalVolume": total_volume,
            "totalValor": total_valor
        }
        
        return self.modelo.converterTiposNumpy(resultado)

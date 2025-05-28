from typing import Dict, List, Optional, Union, Any
import pandas as pd
from dataclasses import dataclass

@dataclass
class ItemProcessamento:
    processo: str
    volume: int
    metodo: Optional[str] = None
    categoriaPai: Optional[str] = None
    ehPai: bool = False


class ModeloProcessamento:
    
    def converterParaDataFrame(self, dados: List[ItemProcessamento]) -> pd.DataFrame:
       
        df = pd.DataFrame([vars(item) for item in dados])
        
        df = df.rename(columns={
            'processo': 'Processo', 
            'volume': 'Volume (L.)', 
            'metodo': 'Método',
            'categoriaPai': 'Categoria_Pai',
            'ehPai': 'is_parent'
        })
        
        return df
    
    @staticmethod
    def converterTiposNumpy(obj: Any) -> Any:
        if hasattr(obj, 'item'):
            return obj.item()
        elif isinstance(obj, dict):
            return {k: ModeloProcessamento.converterTiposNumpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ModeloProcessamento.converterTiposNumpy(i) for i in obj]
        return obj
    
    def estruturarHierarquia(self, df: pd.DataFrame) -> Dict[str, Any]:
        resultado = {}
        processos_pai = df[df['is_parent'] == True]
        processos_filho = df[df['is_parent'] == False]
        
        for _, processo in processos_pai.iterrows():
            nome_processo = processo['Processo']
            filhos_processo = processos_filho[processos_filho['Categoria_Pai'] == nome_processo]
            
            subprocessos = []
            for _, filho in filhos_processo.iterrows():
                subprocessos.append({
                    'processo': filho['Processo'],
                    'volume': int(filho['Volume (L.)'])
                })
            
            resultado[nome_processo] = {
                'processo': nome_processo,
                'volume': int(processo['Volume (L.)']),
                'subprocessos': subprocessos
            }
            
        return resultado

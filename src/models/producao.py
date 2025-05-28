from typing import Dict, List, Optional, Union, Any
import pandas as pd
from dataclasses import dataclass

@dataclass
class ItemProducao:
    produto: str
    quantidade: int
    categoriaPai: Optional[str] = None
    ehPai: bool = False


class ModeloProducao:
    def converterParaDataFrame(self, dados: List[ItemProducao]) -> pd.DataFrame:
        df = pd.DataFrame([vars(item) for item in dados])
        
        df = df.rename(columns={
            'produto': 'Produto', 
            'quantidade': 'Quantidade (L.)', 
            'categoriaPai': 'Categoria_Pai',
            'ehPai': 'is_parent'
        })
        
        return df
    
    @staticmethod
    def converterTiposNumpy(obj: Any) -> Any:
        if hasattr(obj, 'item'):
            return obj.item()
        elif isinstance(obj, dict):
            return {k: ModeloProducao.converterTiposNumpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ModeloProducao.converterTiposNumpy(i) for i in obj]
        return obj

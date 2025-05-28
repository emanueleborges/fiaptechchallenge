
from typing import Dict, List, Optional, Union, Any
import pandas as pd
from dataclasses import dataclass

@dataclass
class ItemComercializacao:
    produto: str
    quantidade: int
    destino: Optional[str] = None
    categoriaPai: Optional[str] = None
    ehPai: bool = False


class ModeloComercializacao:
    
    def converterParaDataFrame(self, dados: List[ItemComercializacao]) -> pd.DataFrame:
       
        df = pd.DataFrame([vars(item) for item in dados])
        
        df = df.rename(columns={
            'produto': 'Produto', 
            'quantidade': 'Quantidade (L.)', 
            'destino': 'Destino',
            'categoriaPai': 'Categoria_Pai',
            'ehPai': 'is_parent'
        })
        
        return df
    
    @staticmethod
    def converterTiposNumpy(obj: Any) -> Any:
       
        if isinstance(obj, dict):
            return {k: ModeloComercializacao.converterTiposNumpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ModeloComercializacao.converterTiposNumpy(i) for i in obj]
        elif str(type(obj)).startswith("<class 'numpy"):
            return obj.item()
        else:
            return obj
    
    def estruturarHierarquia(self, df: pd.DataFrame) -> Dict[str, Any]:
        
        hierarquia = {}
        produtos_pais = df[df['is_parent'] == True]
        
        for _, pai in produtos_pais.iterrows():
            nome_pai = pai['Produto']
            hierarquia[nome_pai] = {
                'quantidade': int(pai['Quantidade (L.)']),
                'destinos': []
            }
            
            # Encontrar os filhos deste pai
            filhos = df[(df['is_parent'] == False) & (df['Categoria_Pai'] == nome_pai)]
            for _, filho in filhos.iterrows():
                hierarquia[nome_pai]['destinos'].append({
                    'produto': filho['Produto'],
                    'quantidade': int(filho['Quantidade (L.)']),
                    'destino': filho['Destino'] if 'Destino' in filho and pd.notna(filho['Destino']) else None
                })
                
        return hierarquia

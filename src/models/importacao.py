
from typing import Dict, List, Optional, Union, Any
import pandas as pd
from dataclasses import dataclass

@dataclass
class ItemImportacao:
    pais: str
    quantidade: int
    valor: float
    categoriaPai: Optional[str] = None
    ehPai: bool = False


class ModeloImportacao:
    
    def converterParaDataFrame(self, dados: List[ItemImportacao]) -> pd.DataFrame:
        
        df = pd.DataFrame([vars(item) for item in dados])
        
        df = df.rename(columns={
            'pais': 'País', 
            'quantidade': 'Quantidade (Kg)', 
            'valor': 'Valor (US$)',
            'categoriaPai': 'Categoria_Pai',
            'ehPai': 'is_parent'
        })
        
        return df
    
    @staticmethod
    def converterTiposNumpy(obj: Any) -> Any:
       
        if isinstance(obj, dict):
            return {k: ModeloImportacao.converterTiposNumpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ModeloImportacao.converterTiposNumpy(i) for i in obj]
        elif str(type(obj)).startswith("<class 'numpy"):
            return obj.item()
        else:
            return obj
    
    def estruturarHierarquia(self, df: pd.DataFrame) -> Dict[str, Any]:
        
        hierarquia = {}
        paises = df[df['País'] != 'Total']
        
        for _, linha in paises.iterrows():
            nome_pais = linha['País']
            hierarquia[nome_pais] = {
                'quantidade': int(linha['Quantidade (Kg)']) if pd.notna(linha['Quantidade (Kg)']) else 0,
                'valor': float(linha['Valor (US$)']) if pd.notna(linha['Valor (US$)']) else 0.0
            }
                
        return hierarquia

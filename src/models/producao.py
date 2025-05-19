"""
Modelo para representar dados de produção de vinhos e derivados.
"""
from typing import Dict, List, Optional, Union, Any
import pandas as pd
from dataclasses import dataclass

@dataclass
class ItemProducao:
    """Representa um item de produção de vinho ou derivado."""
    produto: str
    quantidade: int
    categoriaPai: Optional[str] = None
    ehPai: bool = False


class ModeloProducao:
    """Classe que gerencia os dados de produção obtidos da Embrapa."""
    
    def converterParaDataFrame(self, dados: List[ItemProducao]) -> pd.DataFrame:
        """
        Converte uma lista de ItemProducao para DataFrame.
        
        Args:
            dados: Lista de objetos ItemProducao
            
        Returns:
            DataFrame pandas com os dados formatados
        """
        df = pd.DataFrame([vars(item) for item in dados])
        
        # Renomeia as colunas para o formato esperado
        df = df.rename(columns={
            'produto': 'Produto', 
            'quantidade': 'Quantidade (L.)', 
            'categoriaPai': 'Categoria_Pai',
            'ehPai': 'is_parent'
        })
        
        return df
    
    @staticmethod
    def converterTiposNumpy(obj: Any) -> Any:
        """
        Converte tipos NumPy para tipos Python nativos.
        
        Args:
            obj: Objeto que pode conter tipos NumPy
            
        Returns:
            Objeto com tipos NumPy convertidos para tipos nativos Python
        """
        if hasattr(obj, 'item'):
            return obj.item()  # Converte numpy.int64, numpy.float64, etc. para Python int/float
        elif isinstance(obj, dict):
            return {k: ModeloProducao.converterTiposNumpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ModeloProducao.converterTiposNumpy(i) for i in obj]
        return obj

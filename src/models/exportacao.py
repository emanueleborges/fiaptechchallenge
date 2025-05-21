"""
Modelo para representar dados de exportação de vinhos e derivados.
"""
from typing import Dict, List, Optional, Union, Any
import pandas as pd
from dataclasses import dataclass

@dataclass
class ItemExportacao:
    """Representa um item de exportação de vinho ou derivado."""
    pais: str
    quantidade: int
    valor: float
    categoriaPai: Optional[str] = None
    ehPai: bool = False


class ModeloExportacao:
    """Classe que gerencia os dados de exportação obtidos da Embrapa."""
    
    def converterParaDataFrame(self, dados: List[ItemExportacao]) -> pd.DataFrame:
        """
        Converte uma lista de ItemExportacao para DataFrame.
        
        Args:
            dados: Lista de objetos ItemExportacao
            
        Returns:
            DataFrame pandas com os dados formatados
        """
        df = pd.DataFrame([vars(item) for item in dados])
        
        # Renomeia as colunas para o formato esperado
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
        """
        Converte tipos NumPy para tipos Python nativos.
        
        Args:
            obj: Objeto que pode conter tipos NumPy
            
        Returns:
            Objeto com tipos NumPy convertidos para tipos nativos Python
        """
        if isinstance(obj, dict):
            return {k: ModeloExportacao.converterTiposNumpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ModeloExportacao.converterTiposNumpy(i) for i in obj]
        elif str(type(obj)).startswith("<class 'numpy"):
            return obj.item()
        else:
            return obj
    
    def estruturarHierarquia(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Estrutura os dados do DataFrame em uma hierarquia de países e valores.
        
        Args:
            df: DataFrame com os dados de exportação
            
        Returns:
            Dicionário estruturado hierarquicamente
        """
        hierarquia = {}
        paises = df[df['País'] != 'Total']
        
        for _, linha in paises.iterrows():
            nome_pais = linha['País']
            hierarquia[nome_pais] = {
                'quantidade': int(linha['Quantidade (Kg)']) if pd.notna(linha['Quantidade (Kg)']) else 0,
                'valor': float(linha['Valor (US$)']) if pd.notna(linha['Valor (US$)']) else 0.0
            }
                
        return hierarquia

"""
Modelo para representar dados de importação de vinhos e derivados.
"""
from typing import Dict, List, Optional, Union, Any
import pandas as pd
from dataclasses import dataclass

@dataclass
class ItemImportacao:
    """Representa um item de importação de vinho ou derivado."""
    pais: str
    quantidade: int
    valor: float
    categoriaPai: Optional[str] = None
    ehPai: bool = False


class ModeloImportacao:
    """Classe que gerencia os dados de importação obtidos da Embrapa."""
    
    def converterParaDataFrame(self, dados: List[ItemImportacao]) -> pd.DataFrame:
        """
        Converte uma lista de ItemImportacao para DataFrame.
        
        Args:
            dados: Lista de objetos ItemImportacao
            
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
            return {k: ModeloImportacao.converterTiposNumpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ModeloImportacao.converterTiposNumpy(i) for i in obj]
        elif str(type(obj)).startswith("<class 'numpy"):
            return obj.item()
        else:
            return obj
    
    def estruturarHierarquia(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Estrutura os dados do DataFrame em uma hierarquia de países e valores.
        
        Args:
            df: DataFrame com os dados de importação
            
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

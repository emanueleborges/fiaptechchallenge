"""
Modelo para representar dados de processamento de vinhos e derivados.
"""
from typing import Dict, List, Optional, Union, Any
import pandas as pd
from dataclasses import dataclass

@dataclass
class ItemProcessamento:
    """Representa um item de processamento de vinho ou derivado."""
    processo: str
    volume: int
    metodo: Optional[str] = None
    categoriaPai: Optional[str] = None
    ehPai: bool = False


class ModeloProcessamento:
    """Classe que gerencia os dados de processamento obtidos da Embrapa."""
    
    def converterParaDataFrame(self, dados: List[ItemProcessamento]) -> pd.DataFrame:
        """
        Converte uma lista de ItemProcessamento para DataFrame.
        
        Args:
            dados: Lista de objetos ItemProcessamento
            
        Returns:
            DataFrame pandas com os dados formatados
        """
        df = pd.DataFrame([vars(item) for item in dados])
        
        # Renomeia as colunas para o formato esperado
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
        """
        Converte tipos NumPy para tipos Python nativos.
        
        Args:
            obj: Objeto que pode conter tipos NumPy
            
        Returns:
            Objeto com tipos NumPy convertidos para tipos nativos Python
        """
        if isinstance(obj, dict):
            return {k: ModeloProcessamento.converterTiposNumpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ModeloProcessamento.converterTiposNumpy(i) for i in obj]
        elif str(type(obj)).startswith("<class 'numpy"):
            return obj.item()
        else:
            return obj
    
    def estruturarHierarquia(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Estrutura os dados do DataFrame em uma hierarquia de processos e subprocessos.
        
        Args:
            df: DataFrame com os dados de processamento
            
        Returns:
            Dicionário estruturado hierarquicamente
        """
        hierarquia = {}
        processos_pais = df[df['is_parent'] == True]
        
        for _, pai in processos_pais.iterrows():
            nome_pai = pai['Processo']
            hierarquia[nome_pai] = {
                'volume': int(pai['Volume (L.)']),
                'subprocessos': []
            }
            
            # Encontrar os filhos deste pai
            filhos = df[(df['is_parent'] == False) & (df['Categoria_Pai'] == nome_pai)]
            for _, filho in filhos.iterrows():
                hierarquia[nome_pai]['subprocessos'].append({
                    'processo': filho['Processo'],
                    'volume': int(filho['Volume (L.)']),
                    'metodo': filho['Método'] if 'Método' in filho and pd.notna(filho['Método']) else None
                })
                
        return hierarquia

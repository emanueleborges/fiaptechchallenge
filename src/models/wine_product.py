#!/usr/bin/env python3
"""
Modelos de dados para a aplicação.
"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class WineProduct:
    """
    Modelo para representar um produto de vinho.
    
    Attributes:
        product_name (str): Nome do produto.
        quantity (int): Quantidade em litros.
        year (int): Ano de referência dos dados.
        region (Optional[str]): Região de produção, se disponível.
    """
    product_name: str
    quantity: int
    year: int
    region: Optional[str] = None
    
    @classmethod
    def from_dataframe_row(cls, row, year):
        """
        Cria uma instância do modelo a partir de uma linha do DataFrame.
        
        Args:
            row (pandas.Series): Linha do DataFrame.
            year (int): Ano de referência dos dados.
            
        Returns:
            WineProduct: Instância do modelo.
        """
        return cls(
            product_name=row['Produto'],
            quantity=row['Quantidade (L.)'],
            year=year
        )
    
    def to_dict(self):
        """
        Converte o modelo para um dicionário.
        
        Returns:
            dict: Representação em dicionário do modelo.
        """
        return {
            "produto": self.product_name,
            "quantidade": self.quantity,
            "ano": self.year,
            "regiao": self.region
        }


from typing import Dict, List, Optional, Union, Any
import pandas as pd
from dataclasses import dataclass

@dataclass
class ItemExportacao:
    pais: str
    quantidade: int
    valor: float
    categoriaPai: Optional[str] = None
    ehPai: bool = False


class ModeloExportacao:
    
    def converterParaDataFrame(self, dados: List[ItemExportacao]) -> pd.DataFrame:
        try:
            # Verificar se temos dados válidos
            if not dados:
                print("Aviso: Lista de dados vazia em converterParaDataFrame")
                return pd.DataFrame({
                    'País': [], 
                    'Quantidade (Kg)': [], 
                    'Valor (US$)': [],
                    'Categoria_Pai': [],
                    'is_parent': []
                })
            
            # Tentar criar o DataFrame
            try:
                df = pd.DataFrame([vars(item) if hasattr(item, '__dict__') else item for item in dados])
                print(f"Conversão para DataFrame bem-sucedida. Colunas: {df.columns.tolist()}")
            except Exception as df_error:
                print(f"Erro ao criar DataFrame a partir de objetos: {df_error}")
                # Tentar uma abordagem alternativa
                df = pd.DataFrame(dados)
                print(f"Conversão alternativa realizada. Colunas: {df.columns.tolist()}")
            
            # Garantir que todas as colunas necessárias existam
            required_columns = {
                'pais': 'País', 
                'quantidade': 'Quantidade (Kg)', 
                'valor': 'Valor (US$)',
                'categoriaPai': 'Categoria_Pai',
                'ehPai': 'is_parent'
            }
            
            # Renomear apenas as colunas que existem
            rename_dict = {k: v for k, v in required_columns.items() if k in df.columns}
            if rename_dict:
                df = df.rename(columns=rename_dict)
                print(f"Colunas renomeadas: {rename_dict}")
            
            # Adicionar colunas ausentes com valores padrão
            for new_col, old_col in required_columns.items():
                if old_col not in df.columns and new_col not in df.columns:
                    if old_col in ['Quantidade (Kg)', 'Valor (US$)']:
                        df[old_col] = 0
                    elif old_col in ['is_parent']:
                        df[old_col] = False
                    else:
                        df[old_col] = None
                    print(f"Coluna ausente '{old_col}' adicionada com valores padrão")
            
            return df
        except Exception as e:
            import traceback
            print(f"Erro em converterParaDataFrame: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            # Retornar um DataFrame vazio em caso de erro
            return pd.DataFrame({
                'País': [], 
                'Quantidade (Kg)': [], 
                'Valor (US$)': [],
                'Categoria_Pai': [],
                'is_parent': []
            })
    
    @staticmethod
    def converterTiposNumpy(obj: Any) -> Any:
       
        if isinstance(obj, dict):
            return {k: ModeloExportacao.converterTiposNumpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ModeloExportacao.converterTiposNumpy(i) for i in obj]
        elif str(type(obj)).startswith("<class 'numpy"):
            return obj.item()
        else:
            return obj
    
    def estruturarHierarquia(self, df: pd.DataFrame) -> Dict[str, Any]:
        try:
            hierarquia = {}
            # Verificar as colunas disponíveis
            print(f"Colunas disponíveis para estruturarHierarquia: {df.columns.tolist()}")
            
            # Garantir que as colunas necessárias existam
            if 'País' not in df.columns and 'pais' in df.columns:
                df = df.rename(columns={'pais': 'País'})
                print("Coluna 'pais' renomeada para 'País'")
            
            if 'Quantidade (Kg)' not in df.columns and 'quantidade' in df.columns:
                df = df.rename(columns={'quantidade': 'Quantidade (Kg)'})
                print("Coluna 'quantidade' renomeada para 'Quantidade (Kg)'")
                
            if 'Valor (US$)' not in df.columns and 'valor' in df.columns:
                df = df.rename(columns={'valor': 'Valor (US$)'})
                print("Coluna 'valor' renomeada para 'Valor (US$)'")
            
            # Filtrar os países, excluindo o Total
            paises = df[df['País'] != 'Total'] if 'País' in df.columns else df
            
            # Construir a hierarquia
            for _, linha in paises.iterrows():
                nome_pais = linha['País'] if 'País' in linha else "País Desconhecido"
                
                qtd_key = 'Quantidade (Kg)' if 'Quantidade (Kg)' in linha else 'quantidade' if 'quantidade' in linha else None
                valor_key = 'Valor (US$)' if 'Valor (US$)' in linha else 'valor' if 'valor' in linha else None
                
                hierarquia[nome_pais] = {
                    'quantidade': int(linha[qtd_key]) if qtd_key and pd.notna(linha[qtd_key]) else 0,
                    'valor': float(linha[valor_key]) if valor_key and pd.notna(linha[valor_key]) else 0.0
                }
                    
            return hierarquia
        except Exception as e:
            import traceback
            print(f"Erro em estruturarHierarquia: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            # Retornar uma estrutura vazia em caso de erro
            return {"erro": str(e)}

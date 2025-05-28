import pandas as pd
from typing import Dict, Any, List

from src.models.exportacao import ModeloExportacao
from src.config.configuracao import Configuracao

class ControladorExportacao:
    def __init__(self):
        self.modelo = ModeloExportacao()
    
    def formatarDados(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        try:
            # Fazer uma cópia segura e verificar as colunas
            df = df_dados.copy()
            print(f"Colunas disponíveis no DataFrame original: {df.columns.tolist()}")
            
            # Garantir que todas as colunas esperadas existam no DataFrame
            # Se 'volume' existir e 'quantidade' não existir, renomear
            if 'volume' in df.columns and 'quantidade' not in df.columns:
                df = df.rename(columns={'volume': 'quantidade'})
                print("Coluna 'volume' renomeada para 'quantidade'")
            
            # Se nem 'volume' nem 'quantidade' existirem, criar 'quantidade' com zeros
            if 'quantidade' not in df.columns:
                print("Criando coluna 'quantidade' com zeros")
                df['quantidade'] = 0
                
            # Garantir que 'valor' exista
            if 'valor' not in df.columns:
                print("Criando coluna 'valor' com zeros")
                df['valor'] = 0.0
            
            # Mostrar informações detalhadas para depuração
            print(f"Colunas após correções: {df.columns.tolist()}")
            print(f"Primeiras linhas do DataFrame:\n{df.head().to_string()}")
            
            # Extrair dados da linha total
            linha_total = df[df['pais'] == 'Total']
            if not linha_total.empty:
                print(f"Dados da linha total: {linha_total.iloc[0].to_dict()}")
                total_volume = int(linha_total.iloc[0]['quantidade']) if not linha_total.empty else 0
                total_valor = float(linha_total.iloc[0]['valor']) if not linha_total.empty else 0.0
            else:
                print("Linha total não encontrada. Usando valores padrão.")
                total_volume = 0
                total_valor = 0.0
            
            # Filtrar os dados para processamento
            df = df[df['pais'] != 'Total']
            if hasattr(Configuracao, 'PAISES_IGNORADOS'):
                df = df[~df['pais'].isin(Configuracao.PAISES_IGNORADOS)]
            
            # Construir a estrutura de saída
            itens = []
            for _, linha in df.iterrows():
                pais = linha['pais']
                # Conversão segura para tipos numéricos
                try:
                    volume = int(linha['quantidade'])
                except (ValueError, TypeError):
                    volume = 0
                    
                try:
                    valor = float(linha['valor'])
                except (ValueError, TypeError):
                    valor = 0.0
                
                itens.append({
                    "produto": pais,
                    "quantidade": volume,
                    "valor": valor,
                    "subitem": []
                })
            
            resultado = {
                "Total": total_volume,
                "TotalValor": total_valor,
                "itens": itens
            }
            
            return self.modelo.converterTiposNumpy(resultado)
        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            print(f"ERRO em formatarDados: {str(e)}")
            print(f"TRACEBACK: {error_traceback}")
            
            # Construir informações detalhadas sobre o DataFrame
            df_info = "DataFrame não disponível"
            if 'df_dados' in locals() and df_dados is not None:
                try:
                    df_info = f"Colunas: {df_dados.columns.tolist()}, Linhas: {len(df_dados)}"
                    if len(df_dados) > 0:
                        df_info += f", Amostra primeira linha: {df_dados.iloc[0].to_dict()}"
                except Exception as df_error:
                    df_info = f"Erro ao acessar dados do DataFrame: {str(df_error)}"
            
            # Retornar erro estruturado
            return {
                "erro": f"Erro ao formatar dados de exportação: {str(e)}",
                "df_info": df_info,
                "traceback": error_traceback
            }
    
    def obterDadosHierarquicos(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        try:
            # Fazer uma cópia segura e verificar as colunas
            df = df_dados.copy()
            print(f"Colunas disponíveis no DataFrame original (hierárquico): {df.columns.tolist()}")
            
            # Garantir que todas as colunas esperadas existam no DataFrame
            # Se 'volume' existir e 'quantidade' não existir, renomear
            if 'volume' in df.columns and 'quantidade' not in df.columns:
                df = df.rename(columns={'volume': 'quantidade'})
                print("Coluna 'volume' renomeada para 'quantidade'")
                # Atualizar df_dados para operações subsequentes
                df_dados = df
            
            # Se nem 'volume' nem 'quantidade' existirem, criar 'quantidade' com zeros
            if 'quantidade' not in df.columns:
                print("Criando coluna 'quantidade' com zeros")
                df['quantidade'] = 0
                df_dados = df
                
            # Garantir que 'valor' exista
            if 'valor' not in df.columns:
                print("Criando coluna 'valor' com zeros")
                df['valor'] = 0.0
                df_dados = df
            
            # Mostrar informações detalhadas para depuração
            print(f"Colunas após correções (hierárquico): {df.columns.tolist()}")
            print(f"Primeiras linhas do DataFrame (hierárquico):\n{df.head().to_string()}")
            
            # Converter para o formato esperado pelo modelo
            df_formatado = self.modelo.converterParaDataFrame(df_dados.to_dict('records'))
            print(f"Colunas após conversão para DataFrame formatado: {df_formatado.columns.tolist()}")
            
            # Criar hierarquia
            hierarquia = self.modelo.estruturarHierarquia(df_formatado)
            
            # Extrair dados da linha total
            linha_total = df_dados[df_dados['pais'] == 'Total']
            if not linha_total.empty:
                print(f"Dados da linha total (hierárquico): {linha_total.iloc[0].to_dict()}")
                total_volume = int(linha_total.iloc[0]['quantidade']) if not linha_total.empty else 0
                total_valor = float(linha_total.iloc[0]['valor']) if not linha_total.empty else 0.0
            else:
                print("Linha total não encontrada (hierárquico). Usando valores padrão.")
                total_volume = 0
                total_valor = 0.0
            
            resultado = {
                "paises": hierarquia,
                "totalVolume": total_volume,
                "totalValor": total_valor
            }
            
            return self.modelo.converterTiposNumpy(resultado)
        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            print(f"ERRO em obterDadosHierarquicos: {str(e)}")
            print(f"TRACEBACK: {error_traceback}")
            
            # Construir informações detalhadas sobre o DataFrame
            df_info = "DataFrame não disponível"
            if 'df_dados' in locals() and df_dados is not None:
                try:
                    df_info = f"Colunas: {df_dados.columns.tolist()}, Linhas: {len(df_dados)}"
                    if len(df_dados) > 0:
                        df_info += f", Amostra primeira linha: {df_dados.iloc[0].to_dict()}"
                except Exception as df_error:
                    df_info = f"Erro ao acessar dados do DataFrame: {str(df_error)}"
            
            # Retornar erro estruturado
            return {
                "erro": f"Erro ao obter dados hierárquicos de exportação: {str(e)}",
                "df_info": df_info,
                "traceback": error_traceback
            }

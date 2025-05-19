"""
Controlador responsável pelo processamento dos dados de produção
"""
import pandas as pd
from typing import Dict, List, Any

from src.models.producao import ModeloProducao
from src.config.configuracao import Configuracao

class ControladorProducao:
    def __init__(self):
        self.modelo = ModeloProducao()
    
    def formatarDados(self, df_dados: pd.DataFrame) -> Dict[str, Any]:
        """
        Formata os dados do DataFrame para o formato desejado da API
        
        Args:
            df_dados: DataFrame com os dados de produção
            
        Returns:
            Dicionário formatado para ser convertido em JSON
        """
        # Estruturar os dados hierarquicamente
        resultado = {}
        total = 0
        
        # Extrair o total
        linha_total = df_dados[df_dados['Produto'] == 'Total']
        if not linha_total.empty:
            total = linha_total.iloc[0]['Quantidade (L.)']
            # Remover o Total do DataFrame para processamento
            df_dados = df_dados[df_dados['Produto'] != 'Total']
        
        # Primeiro, processar os produtos pai (exceto os ignorados)
        produtos_pai = df_dados[(df_dados['is_parent']) & 
                              (~df_dados['Produto'].isin(Configuracao.PRODUTOS_IGNORADOS))]
        
        produtos_dict = {}
        
        # Processar os produtos pai primeiro
        indice = 1
        for _, linha in produtos_pai.iterrows():
            nome_item = f"item {indice}"
            objeto_produto = {
                "produto": linha['Produto'],
                "quantidade": linha['Quantidade (L.)'],
                "subitem": []
            }
            resultado[nome_item] = objeto_produto
            produtos_dict[linha['Produto']] = objeto_produto
            indice += 1
        
        # Em seguida, processar os produtos filhos
        produtos_filhos = df_dados[~df_dados['is_parent']]
        for _, linha in produtos_filhos.iterrows():
            categoria_pai = linha['Categoria_Pai']
            # Verificar se o pai está no dicionário
            if categoria_pai in produtos_dict:
                produtos_dict[categoria_pai]['subitem'].append({
                    "produto": linha['Produto'],
                    "quantidade": linha['Quantidade (L.)']
                })
        
        # Adicionar o Total
        resultado["Total"] = int(total)
        
        # Converter todos os valores NumPy antes da serialização
        resultado = self.modelo.converterTiposNumpy(resultado)
        
        # Reformatar o dicionário para o formato desejado com a sintaxe especial "item {"
        formato_final = {}
        itens = {}
        
        # Primeiro, adicionar todos os itens com o formato correto
        for chave, valor in resultado.items():
            if chave.startswith("item "):
                # Recolhemos todos os itens, vamos formatá-los depois
                itens[chave] = valor
            elif chave == "Total":
                formato_final["Total"] = valor
                
        # Agora, formatamos os itens na ordem correta
        for i, (chave, valor) in enumerate(itens.items(), 1):
            # Usar o formato especial "item {"
            formato_final[f"item {i} {{"] = valor
        
        return formato_final

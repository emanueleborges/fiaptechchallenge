"""
Serviço responsável por fazer o web scraping dos dados da Embrapa
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from typing import List, Dict, Any, Tuple

from src.models.producao import ItemProducao
from src.config.configuracao import Configuracao

class ServicoEmbrapa:
    def __init__(self):
        self.urlBase = Configuracao.URL_BASE_EMBRAPA

    def coletarDados(self, ano: int) -> pd.DataFrame:
        """
        Faz o web scraping dos dados da Embrapa para o ano específicado
        
        Args:
            ano (int): O ano para o qual se deseja obter os dados
            
        Returns:
            pd.DataFrame: DataFrame com os dados de produção de vinho
        """
        url = f"{self.urlBase}?ano={ano}&opcao=opt_02"
        resposta = requests.get(url)
        soup = BeautifulSoup(resposta.content, 'html.parser')
        dados = []
        valorTotal = 0
        
        # Variável para armazenar categoria pai atual
        categoriaPaiAtual = None
        
        # Encontrar a tabela de dados
        tabelas = soup.find_all('table', class_='tb_base tb_dados')
        
        for tabela in tabelas:
            # Processar as linhas da tabela
            linhas = tabela.find_all('tr')
            
            for linha in linhas:
                colunas = linha.find_all('td')
                if len(colunas) == 2:
                    # Extrair texto dos campos
                    produto = colunas[0].text.strip()
                    texto_quantidade = colunas[1].text.strip()
                    
                    # Identificar se é um item pai (tb_item) ou filho (tb_subitem)
                    ehPai = 'tb_item' in colunas[0].get('class', [])
                    
                    # Se for Total, salvar o valor e continuar
                    if produto == 'Total':
                        texto_total = texto_quantidade.replace('.', '').replace(',', '.')
                        try:
                            valorTotal = int(float(texto_total))
                        except ValueError:
                            valorTotal = 0
                        continue
                    
                    # Se não for Total e não for cabeçalho "Produto"
                    if produto != 'Produto':
                        # Atualize o pai atual se for um item pai
                        if ehPai:
                            categoriaPaiAtual = produto
                            idPai = None
                        else:
                            idPai = categoriaPaiAtual
                        
                        # Formatar valor numérico
                        if texto_quantidade == '-':
                            quantidade = 0
                        else:
                            # Remove pontos dos números e substitui vírgulas por pontos
                            quantidade_texto = texto_quantidade.replace('.', '').replace(',', '.')
                            try:
                                # Tenta converter para número
                                quantidade = int(float(quantidade_texto))
                            except ValueError:
                                quantidade = 0
                        
                        # Adiciona o produto e sua quantidade aos dados
                        dados.append({
                            'produto': produto,
                            'quantidade': quantidade,
                            'categoriaPai': idPai,
                            'ehPai': ehPai
                        })
        
        # Adicionar Total como um item especial
        dados.append({
            'produto': 'Total',
            'quantidade': valorTotal,
            'categoriaPai': None,
            'ehPai': True
        })
        
        # Criar DataFrame e renomear colunas
        df = pd.DataFrame(dados)
        df = df.rename(columns={
            'produto': 'Produto', 
            'quantidade': 'Quantidade (L.)', 
            'categoriaPai': 'Categoria_Pai',
            'ehPai': 'is_parent'
        })
        
        return df

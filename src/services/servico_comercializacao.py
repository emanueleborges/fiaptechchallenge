"""
Serviço responsável por fazer o web scraping dos dados de comercialização da Embrapa
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from typing import List, Dict, Any, Tuple

from src.models.comercializacao import ItemComercializacao
from src.config.configuracao import Configuracao

class ServicoComercializacao:
    def __init__(self):
        self.urlBase = Configuracao.URL_BASE_EMBRAPA

    def coletarDadosComercializacao(self, ano: int, opcao: str = 'opt_04', subopcao: str = None) -> pd.DataFrame:
        """
        Faz o web scraping dos dados de comercialização da Embrapa para o ano específicado
        
        Args:
            ano (int): O ano para o qual se deseja obter os dados
            opcao (str): Opção do relatório (ex: 'opt_04')
            subopcao (str): Subopção do relatório, se necessário
            
        Returns:
            pd.DataFrame: DataFrame com os dados de comercialização de vinho
        """
        url = f"{self.urlBase}?ano={ano}&opcao={opcao}"
        if subopcao:
            url += f"&subopcao={subopcao}"
            
        resposta = requests.get(url)
        soup = BeautifulSoup(resposta.content, 'html.parser')
        dados = []
        valor_total = 0
        
        # Variável para armazenar categoria pai atual
        categoria_pai_atual = None
        
        # Encontrar a tabela de dados
        tabelas = soup.find_all('table', class_='tb_base tb_dados')
        
        for tabela in tabelas:
            # Processar as linhas da tabela
            linhas = tabela.find_all('tr')
            
            for linha in linhas:
                colunas = linha.find_all('td')
                if len(colunas) >= 2:  # Comercialização pode ter mais colunas
                    # Extrair texto dos campos
                    produto = colunas[0].text.strip()
                    texto_quantidade = colunas[1].text.strip()
                    
                    # Tentar extrair o destino, se existir
                    destino = None
                    if len(colunas) > 2:
                        destino = colunas[2].text.strip() if colunas[2].text.strip() else None
                    
                    # Identificar se é um item pai (tb_item) ou filho (tb_subitem)
                    eh_pai = 'tb_item' in colunas[0].get('class', [])
                    
                    # Ignorar colunas de cabeçalho e produtos específicos ignorados
                    if produto in ['Produto', 'Total'] or produto in Configuracao.PRODUTOS_IGNORADOS:
                        if produto == 'Total':
                            try:
                                valor_total = int(re.sub(r'[^\d]', '', texto_quantidade))
                            except ValueError:
                                valor_total = 0
                        continue
                    
                    # Converter quantidade para inteiro
                    try:
                        quantidade = int(re.sub(r'[^\d]', '', texto_quantidade)) if texto_quantidade.strip() != '-' else 0
                    except ValueError:
                        quantidade = 0
                    
                    # Se for um item pai, atualizar a categoria pai atual
                    if eh_pai:
                        categoria_pai_atual = produto
                        item = ItemComercializacao(
                            produto=produto,
                            quantidade=quantidade,
                            destino=destino,
                            categoriaPai=None,
                            ehPai=True
                        )
                    else:
                        # É um item filho
                        item = ItemComercializacao(
                            produto=produto,
                            quantidade=quantidade,
                            destino=destino,
                            categoriaPai=categoria_pai_atual,
                            ehPai=False
                        )
                    
                    dados.append(item)
        
        # Adicionar o valor total como um item especial
        dados.append(ItemComercializacao(
            produto='Total',
            quantidade=valor_total,
            destino=None,
            categoriaPai=None,
            ehPai=False
        ))
        
        # Converter para DataFrame
        df = pd.DataFrame([vars(item) for item in dados])
        
        return df

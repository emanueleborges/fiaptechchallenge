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

    def coletarDados(self, ano: int, opcao: str = None) -> pd.DataFrame:
        url = f"{self.urlBase}?ano={ano}"
        if opcao is None:
            opcao = Configuracao.OPCAO_PRODUCAO
        
        url += f"&opcao={opcao}"
        resposta = requests.get(url)
        soup = BeautifulSoup(resposta.content, 'html.parser')
        dados = []
        valorTotal = 0
        
        categoriaPaiAtual = None
        
        tabelas = soup.find_all('table', class_='tb_base tb_dados')
        
        for tabela in tabelas:
            linhas = tabela.find_all('tr')
            
            for linha in linhas:
                colunas = linha.find_all('td')
                if len(colunas) == 2:
                    produto = colunas[0].text.strip()
                    texto_quantidade = colunas[1].text.strip()
                    
                    ehPai = 'tb_item' in colunas[0].get('class', [])
                    
                    if produto == 'Total':
                        texto_total = texto_quantidade.replace('.', '').replace(',', '.')
                        try:
                            valorTotal = int(float(texto_total))
                        except ValueError:
                            valorTotal = 0
                        continue
                    
                    if produto != 'Produto':
                        if ehPai:
                            categoriaPaiAtual = produto
                            idPai = None
                        else:
                            idPai = categoriaPaiAtual
                        
                        if texto_quantidade == '-':
                            quantidade = 0
                        else:
                            quantidade_texto = texto_quantidade.replace('.', '').replace(',', '.')
                            try:
                                quantidade = int(float(quantidade_texto))
                            except ValueError:
                                quantidade = 0
                        
                        dados.append({
                            'produto': produto,
                            'quantidade': quantidade,
                            'categoriaPai': idPai,
                            'ehPai': ehPai
                        })
        
        dados.append({
            'produto': 'Total',
            'quantidade': valorTotal,
            'categoriaPai': None,
            'ehPai': True
        })
        
        df = pd.DataFrame(dados)
        df = df.rename(columns={
            'produto': 'Produto', 
            'quantidade': 'Quantidade (L.)', 
            'categoriaPai': 'Categoria_Pai',
            'ehPai': 'is_parent'
        })
        
        return df

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
        url = f"{self.urlBase}?ano={ano}"
        
        url += f"&opcao={opcao}"
        if subopcao:
            url += f"&subopcao={subopcao}"
            
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
                if len(colunas) >= 2:
                    produto = colunas[0].text.strip()
                    texto_quantidade = colunas[1].text.strip()
                    
                    ehPai = 'tb_item' in colunas[0].get('class', [])
                    
                    if produto != 'Produto' and produto not in Configuracao.PRODUTOS_IGNORADOS:
                        if produto == 'Total':
                            texto_total = texto_quantidade.replace('.', '').replace(',', '.')
                            try:
                                valorTotal = int(float(texto_total))
                            except ValueError:
                                valorTotal = 0
                            continue
                        
                        if texto_quantidade == '-':
                            quantidade = 0
                        else:
                            quantidade_texto = texto_quantidade.replace('.', '').replace(',', '.')
                            try:
                                quantidade = int(float(quantidade_texto))
                            except ValueError:
                                quantidade = 0
                        
                        if ehPai:
                            categoriaPaiAtual = produto
                            idPai = None
                        else:
                            idPai = categoriaPaiAtual
                            
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
        
        return df

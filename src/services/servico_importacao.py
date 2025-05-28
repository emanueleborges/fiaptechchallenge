import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from typing import List, Dict, Any, Tuple

from src.models.importacao import ItemImportacao
from src.config.configuracao import Configuracao

class ServicoImportacao:
    def __init__(self):
        self.urlBase = Configuracao.URL_BASE_EMBRAPA

    def coletarDadosImportacao(self, ano: int, opcao: str = None, subopcao: str = None) -> pd.DataFrame:
        url = f"{self.urlBase}?ano={ano}"
        
        if opcao is None:
            opcao = Configuracao.OPCAO_IMPORTACAO
            
        if subopcao is None:
            subopcao = Configuracao.SUBOPCAO_IMPORTACAO_PADRAO
            
        url += f"&opcao={opcao}&subopcao={subopcao}"
        
        resposta = requests.get(url)
        soup = BeautifulSoup(resposta.content, 'html.parser')
        dados = []
        valorTotal = 0
        valorTotalDolar = 0
        
        tabelas = soup.find_all('table', class_='tb_base tb_dados')
        
        for tabela in tabelas:
            linhas = tabela.find_all('tr')
            
            for linha in linhas:
                colunas = linha.find_all('td')
                if len(colunas) >= 3:
                    pais = colunas[0].text.strip()
                    texto_quantidade = colunas[1].text.strip() if len(colunas) > 1 else '0'
                    texto_valor = colunas[2].text.strip() if len(colunas) > 2 else '0'
                    
                    if pais not in Configuracao.PAISES_IGNORADOS:
                        if pais == 'Total':
                            try:
                                valorTotal = int(float(texto_quantidade.replace('.', '').replace(',', '.')))
                                valorTotalDolar = float(texto_valor.replace('.', '').replace(',', '.'))
                            except (ValueError, IndexError):
                                valorTotal = 0
                                valorTotalDolar = 0
                            continue
                        
                        quantidade = 0
                        if texto_quantidade != '-':
                            try:
                                quantidade = int(float(texto_quantidade.replace('.', '').replace(',', '.')))
                            except ValueError:
                                quantidade = 0
                        
                        valor = 0.0
                        if texto_valor != '-':
                            try:
                                valor = float(texto_valor.replace('.', '').replace(',', '.'))
                            except ValueError:
                                valor = 0.0
                        
                        dados.append({
                            'pais': pais,
                            'quantidade': quantidade,
                            'valor': valor
                        })
        
        dados.append({
            'pais': 'Total',
            'quantidade': valorTotal,
            'valor': valorTotalDolar
        })
        
        df = pd.DataFrame(dados)
        
        return df

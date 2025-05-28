import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from typing import List, Dict, Any, Tuple

from src.models.processamento import ItemProcessamento
from src.config.configuracao import Configuracao

class ServicoProcessamento:
    def __init__(self):
        self.urlBase = Configuracao.URL_BASE_EMBRAPA

    def coletarDadosProcessamento(self, ano: int, opcao: str = 'opt_03', subopcao: str = None) -> pd.DataFrame:
        url = f"{self.urlBase}?ano={ano}"
        
        if subopcao is None:
            subopcao = Configuracao.SUBOPCAO_PROCESSAMENTO_PADRAO
            
        url += f"&opcao={opcao}&subopcao={subopcao}"
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
                    processo = colunas[0].text.strip()
                    texto_volume = colunas[1].text.strip()
                    
                    metodo = ''
                    if len(colunas) > 2:
                        metodo = colunas[2].text.strip()
                    
                    ehPai = 'tb_item' in colunas[0].get('class', [])
                    
                    if processo != 'Processo' and processo != 'Total' and processo not in Configuracao.PROCESSOS_IGNORADOS:
                        if texto_volume == '-':
                            volume = 0
                        else:
                            volume_texto = texto_volume.replace('.', '').replace(',', '.')
                            try:
                                volume = int(float(volume_texto))
                            except ValueError:
                                volume = 0
                        
                        if ehPai:
                            categoriaPaiAtual = processo
                            idPai = None
                        else:
                            idPai = categoriaPaiAtual
                            
                        dados.append({
                            'processo': processo,
                            'volume': volume,
                            'metodo': metodo,
                            'categoriaPai': idPai,
                            'ehPai': ehPai
                        })
                    elif processo == 'Total':
                        texto_total = texto_volume.replace('.', '').replace(',', '.')
                        try:
                            valorTotal = int(float(texto_total))
                        except ValueError:
                            valorTotal = 0
        
        dados.append({
            'processo': 'Total',
            'volume': valorTotal,
            'metodo': '',
            'categoriaPai': None,
            'ehPai': True
        })
        
        df = pd.DataFrame(dados)
        
        return df

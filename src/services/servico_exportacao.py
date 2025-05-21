"""
Serviço responsável por fazer o web scraping dos dados de exportação da Embrapa
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from typing import List, Dict, Any, Tuple

from src.models.exportacao import ItemExportacao
from src.config.configuracao import Configuracao

__all__ = ['ServicoExportacao']

class ServicoExportacao:
    def __init__(self):
        self.urlBase = Configuracao.URL_BASE_EMBRAPA

    def coletarDadosExportacao(self, ano: int, opcao: str = None, subopcao: str = None) -> pd.DataFrame:
        """
        Faz o web scraping dos dados de exportação da Embrapa para o ano específicado
        
        Args:
            ano (int): O ano para o qual se deseja obter os dados
            opcao (str): Opção do relatório (padrão: 'opt_06')
            subopcao (str): Subopção do relatório (padrão: 'subopt_03')
            
        Returns:
            pd.DataFrame: DataFrame com os dados de exportação de vinho
        """
        # Usar valores padrão da configuração se não forem especificados
        if opcao is None:
            opcao = Configuracao.OPCAO_EXPORTACAO
        if subopcao is None:
            subopcao = Configuracao.SUBOPCAO_EXPORTACAO_PADRAO
            
        url = f"{self.urlBase}?ano={ano}&opcao={opcao}&subopcao={subopcao}"
        resposta = requests.get(url)
        soup = BeautifulSoup(resposta.content, 'html.parser')
        dados = []
        
        quantidade_total = 0
        valor_total = 0.0
        
        # Encontrar a tabela de dados
        tabelas = soup.find_all('table', class_='tb_base tb_dados')
        
        for tabela in tabelas:
            # Processar as linhas da tabela
            linhas = tabela.find_all('tr')
            
            for linha in linhas:
                colunas = linha.find_all('td')
                if len(colunas) >= 3:  # Exportação tem 3 colunas (País, Quantidade, Valor)
                    # Extrair texto dos campos
                    pais = colunas[0].text.strip()
                    texto_quantidade = colunas[1].text.strip()
                    texto_valor = colunas[2].text.strip()
                    
                    # Identificar se é um item pai ou total
                    ehPai = False
                    
                    # Ignorar colunas de cabeçalho e produtos específicos ignorados
                    if pais in ['País', 'Países', 'Total'] or pais in Configuracao.PAISES_IGNORADOS:
                        if pais == 'Total':
                            try:
                                quantidade_total = int(re.sub(r'[^\d]', '', texto_quantidade)) if texto_quantidade.strip() != '-' else 0
                                # Remover pontos/vírgulas e converter para float
                                valor_texto = texto_valor.replace('.', '').replace(',', '.')
                                valor_total = float(valor_texto) if texto_valor.strip() != '-' else 0.0
                            except ValueError:
                                quantidade_total = 0
                                valor_total = 0.0
                        continue
                    
                    # Converter quantidade para inteiro
                    try:
                        quantidade = int(re.sub(r'[^\d]', '', texto_quantidade)) if texto_quantidade.strip() != '-' else 0
                    except ValueError:
                        quantidade = 0
                        
                    # Converter valor para float (substituindo pontos e vírgulas)
                    try:
                        if texto_valor.strip() == '-':
                            valor = 0.0
                        else:
                            # Remover pontos e substituir vírgulas por pontos
                            valor_texto = texto_valor.replace('.', '').replace(',', '.')
                            valor = float(valor_texto)
                    except ValueError:
                        valor = 0.0
                    
                    # Criar item de exportação
                    item = ItemExportacao(
                        pais=pais,
                        quantidade=quantidade,
                        valor=valor,
                        categoriaPai=None,
                        ehPai=ehPai
                    )
                    
                    dados.append(item)
        
        # Adicionar linha do total
        total = ItemExportacao(
            pais='Total',
            quantidade=quantidade_total,
            valor=valor_total,
            categoriaPai=None,
            ehPai=True
        )
        
        dados.append(total)
        
        # Converter para DataFrame
        df_dados = pd.DataFrame([vars(item) for item in dados])
        
        return df_dados

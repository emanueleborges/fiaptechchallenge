#!/usr/bin/env python3
"""
Serviço para extração de dados do site da Embrapa.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from src.config.settings import logger

def crawl_embrapa(year):
    """
    Extrai dados de produção de vinhos do site da Embrapa para o ano especificado.
    
    Args:
        year (int): Ano para o qual os dados serão extraídos.
        
    Returns:
        pandas.DataFrame: DataFrame contendo produtos e quantidades de produção.
        
    Raises:
        requests.RequestException: Se ocorrer erro na requisição HTTP.
    """
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02"
    logger.info(f"Crawling Embrapa data for year {year} from {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Verifica se a resposta HTTP é válida
    except requests.RequestException as e:
        logger.error(f"Failed to fetch data from Embrapa: {e}")
        raise
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    data = []
    tables = soup.find_all('table', class_='tb_base')
    
    if not tables:
        logger.warning(f"No data tables found for year {year}")
    
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if len(cols) == 2 and cols[0] != 'Produto' and cols[0] != 'Total':
                product = cols[0]
                quantity = cols[1].replace('.', '').replace('-', '0')  # Remove dots and replace '-' with 0
                try:
                    quantity = int(quantity)
                except ValueError:
                    logger.warning(f"Could not convert quantity '{cols[1]}' to int for product '{product}'. Setting to 0.")
                    quantity = 0  # if conversion fails, set to 0
                data.append([product, quantity])
    
    df = pd.DataFrame(data, columns=['Produto', 'Quantidade (L.)'])
    logger.info(f"Retrieved {len(df)} products for year {year}")
    return df

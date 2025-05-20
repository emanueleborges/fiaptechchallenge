#!/usr/bin/env python3
"""
Serviço para extração de dados do site da Embrapa.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from src.config.settings import logger

def crawl_embrapa(year, hierarchical=True):
    """
    Extrai dados de produção de vinhos do site da Embrapa para o ano especificado.
    
    Args:
        year (int): Ano para o qual os dados serão extraídos.
        hierarchical (bool): Se True, retorna os dados em formato hierárquico pai-filho.
        
    Returns:
        dict/DataFrame: Se hierarchical=True, retorna um dicionário com estrutura 
        hierárquica. Caso contrário, retorna um DataFrame.
        
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
    
    # Se não for solicitada a estrutura hierárquica, retorna o DataFrame original
    if not hierarchical:
        return df
    
    # Processamento para criar a estrutura hierárquica
    return create_hierarchical_structure(df, year)

def create_hierarchical_structure(df, year):
    """
    Processa o DataFrame e cria uma estrutura hierárquica pai-filho.
    
    Args:
        df (pandas.DataFrame): DataFrame com os produtos e quantidades.
        year (int): Ano dos dados para incluir no resultado.
        
    Returns:
        dict: Estrutura de dados hierárquica em formato JSON.
    """
    hierarchical_data = {
        "ano": year,
        "data": [],
        "total": 0
    }
    
    # Identificar produtos pai e filhos
    current_parent = None
    parent_index = -1
    
    # Verificar cada linha para determinar se é pai ou filho
    for _, row in df.iterrows():
        product = row['Produto']
        quantity = row['Quantidade (L.)']
        
        # Adiciona ao total geral
        hierarchical_data["total"] += quantity
        
        # Se o nome do produto estiver todo em maiúsculas, é um produto pai
        # Ou se começar com espaços em branco, é um filho
        if product.isupper() or (current_parent is None and not product.startswith(' ')):
            # É um produto pai
            current_parent = {
                "nome": product.strip(),
                "quantidade": quantity,
                "filhos": []
            }
            hierarchical_data["data"].append(current_parent)
            parent_index += 1
        else:
            # É um produto filho
            if current_parent is not None:
                child = {
                    "nome": product.strip(),
                    "quantidade": quantity
                }
                hierarchical_data["data"][parent_index]["filhos"].append(child)
    
    # Verifica e corrige a estrutura para garantir que todos os produtos estejam categorizados corretamente
    fix_hierarchical_structure(hierarchical_data)
    
    return hierarchical_data

def fix_hierarchical_structure(data):
    """
    Corrige possíveis problemas na estrutura hierárquica.
    
    Args:
        data (dict): Estrutura de dados hierárquica.
    """
    # Se algum produto pai não tiver filhos mas tiver quantidade,
    # verifica se ele pode ser movido como filho de outro produto
    for i in range(len(data["data"])):
        if not data["data"][i]["filhos"] and data["data"][i]["quantidade"] > 0:
            continue  # Se não tem filhos mas tem quantidade, é um produto independente
            
        # Verifica produtos sem quantidade própria
        if data["data"][i]["quantidade"] == 0 and not data["data"][i]["filhos"]:
            # Possivelmente é um filho incorretamente classificado como pai
            # Tentamos encontrar um pai apropriado
            for j in range(len(data["data"])):
                if i != j and data["data"][i]["nome"] in data["data"][j]["nome"]:
                    # Move como filho
                    data["data"][j]["filhos"].append({
                        "nome": data["data"][i]["nome"],
                        "quantidade": data["data"][i]["quantidade"]
                    })
                    # Marca para remoção
                    data["data"][i] = None
                    break
    
    # Remove produtos marcados como None
    data["data"] = [item for item in data["data"] if item is not None]

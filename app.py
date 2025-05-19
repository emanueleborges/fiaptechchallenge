#!/usr/bin/env python3
# filepath: c:\Users\emanuel.borges\Desktop\Outros\Fiap\app.py
"""
API para extrair dados de produção de vinhos do site da Embrapa.
Fornece endpoints para consulta de dados em formato JSON.
"""
import logging
import os
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Inicialização da aplicação Flask
app = Flask(__name__)
CORS(app)  # Permitir requisições cross-origin

# Configuração de ambiente
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
PORT = int(os.environ.get('PORT', 5000))
HOST = os.environ.get('HOST', '0.0.0.0')

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

@app.route('/embrapa_data', methods=['GET'])
def get_embrapa_data():
    """
    Endpoint para obter dados de produção de vinhos da Embrapa.
    
    Query Parameters:
        ano (int, optional): Ano para filtrar os dados. Default: 2023.
        
    Returns:
        Response: Dados em formato JSON.
    """
    try:
        year = request.args.get('ano', default=2023, type=int)
        logger.info(f"Received request for Embrapa data with year={year}")
        
        df_data = crawl_embrapa(year)
        json_output = df_data.to_json(orient='records', indent=4, force_ascii=False)
        
        return Response(json_output, mimetype='application/json')
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return jsonify({"error": "Failed to retrieve data", "details": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificar o status da aplicação.
    
    Returns:
        Response: Status da aplicação em formato JSON.
    """
    return jsonify({
        "status": "healthy",
        "service": "embrapa-crawler"
    })

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Handler global para exceções HTTP."""
    logger.error(f"HTTP error: {e}")
    return jsonify({"error": e.description}), e.code

@app.errorhandler(Exception)
def handle_exception(e):
    """Handler global para exceções não tratadas."""
    logger.error(f"Unhandled exception: {e}", exc_info=True)
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    logger.info(f"Starting Embrapa Crawler API on {HOST}:{PORT} (debug={DEBUG})")
    app.run(host=HOST, port=PORT, debug=DEBUG)

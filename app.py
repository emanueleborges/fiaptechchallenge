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
import json
from flask import Flask, request, Response
from src.config import Config
from src.controllers.routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == '__main__':
    logger.info(f"Starting Embrapa Crawler API on {HOST}:{PORT} (debug={DEBUG})")
    app.run(host=HOST, port=PORT, debug=DEBUG)

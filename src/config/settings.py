#!/usr/bin/env python3
"""
Configurações da aplicação.
"""
import os
import logging
import sys

# Configurações de ambiente
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
PORT = int(os.environ.get('PORT', 5000))
HOST = os.environ.get('HOST', '0.0.0.0')

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

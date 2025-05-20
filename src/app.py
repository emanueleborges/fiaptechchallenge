#!/usr/bin/env python3
"""
Inicialização da aplicação Flask.
"""
from flask import Flask
from flask_cors import CORS
from src.routes.api_routes import api_routes
from src.utils.error_handlers import register_error_handlers

def create_app():
    """
    Cria e configura a aplicação Flask.
    
    Returns:
        Flask: Instância da aplicação Flask configurada.
    """
    app = Flask(__name__)
    CORS(app)  # Permitir requisições cross-origin
    
    # Registrando as rotas
    app.register_blueprint(api_routes)
    
    # Registrando handlers de erro
    register_error_handlers(app)
    
    return app

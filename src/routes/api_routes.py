#!/usr/bin/env python3
"""
Rotas da API.
"""
from flask import Blueprint
from src.controllers.embrapa_controller import get_embrapa_data_controller, health_check_controller

# Criando Blueprint para as rotas da API
api_routes = Blueprint('api', __name__)

# Registrando as rotas
api_routes.route('/embrapa_data', methods=['GET'])(get_embrapa_data_controller)
api_routes.route('/health', methods=['GET'])(health_check_controller)

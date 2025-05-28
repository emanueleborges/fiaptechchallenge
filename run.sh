#!/bin/bash

# Script para executar a aplicação Flask
# Pode ser usado tanto em desenvolvimento quanto em produção

# Verifica se estamos em modo de desenvolvimento ou produção
if [ "$DEBUG" = "true" ] || [ "$DEBUG" = "True" ]; then
    echo "Executando em modo de desenvolvimento..."
    python app.py
else
    echo "Executando em modo de produção com Gunicorn..."
    gunicorn --bind ${HOST:-0.0.0.0}:${PORT:-5000} \
             --workers ${WORKERS:-4} \
             --threads ${THREADS:-2} \
             --timeout ${TIMEOUT:-120} \
             --access-logfile - \
             --error-logfile - \
             app:app
fi

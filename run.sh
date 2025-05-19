#!/bin/bash
# filepath: c:\Users\emanuel.borges\Desktop\Outros\Fiap\run.sh

# Executa o servidor gunicorn em modo de produção
gunicorn --bind 0.0.0.0:5000 --workers 4 --threads 2 --timeout 120 app:app

# Use Python 3.9 slim as base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=5000 \
    HOST=0.0.0.0 \
    DEBUG=False \
    EMBRAPA_BASE_URL=http://vitibrasil.cnpuv.embrapa.br/index.php \
    API_EMBRAPA_DATA_URL=/embrapa_data?data={data}&opcao={opcao} \
    API_HEALTH_URL=/health \
    ANO_PADRAO=2023 \
    OPCAO_PRODUCAO=opt_02 \
    OPCAO_PROCESSAMENTO=opt_03 \
    OPCAO_COMERCIALIZACAO=opt_04 \
    OPCAO_IMPORTACAO=opt_05 \
    OPCAO_EXPORTACAO=opt_06 \
    SUBOPCAO_PROCESSAMENTO_PADRAO=subopt_03 \
    SUBOPCAO_IMPORTACAO_PADRAO=subopt_03 \
    SUBOPCAO_EXPORTACAO_PADRAO=subopt_03 \
    PRODUTOS_IGNORADOS="Dados da Vitivinicultura,DOWNLOAD" \
    PROCESSOS_IGNORADOS="Dados da Vitivinicultura,DOWNLOAD" \
    PAISES_IGNORADOS="Dados da Vitivinicultura,DOWNLOAD,Não consta na tabela" \
    FORMATOS_RESPOSTA="padrao,hierarquico" \
    TIMEOUT=120 \
    WORKERS=4 \
    THREADS=2

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN adduser --disabled-password --gecos "" appuser

# Copy and install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Make run.sh executable
RUN chmod +x run.sh

# Change ownership to the non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application with Gunicorn in production
CMD ["sh", "run.sh"]

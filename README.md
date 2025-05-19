# Embrapa Data Crawler API

Uma API baseada em Flask para extrair e disponibilizar dados de produção de vinhos do site da Embrapa.

## Funcionalidades

- Web crawler para dados de produção de vinhos da Embrapa
- API RESTful com respostas em formato JSON
- Filtragem de dados por ano
- Tratamento de erros e logging
- Suporte a Docker para fácil implantação
- Testes unitários
- Validação de código com flake8 e mypy

## Instalação

### Pré-requisitos

- Python 3.9+
- pip (gerenciador de pacotes Python)

### Configuração Local

1. Clone este repositório:
   ```bash
   git clone <repository-url>
   cd Fiap
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   # No Windows
   python -m venv .venv
   .venv\Scripts\activate

   # No macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```bash
   python app.py
   ```

   Ou em modo de produção:
   ```bash
   # No Windows
   gunicorn --bind 0.0.0.0:5000 --workers 4 --threads 2 app:app
   
   # No macOS/Linux
   sh run.sh
   ```

### Configuração com Docker

1. Construa a imagem Docker:
   ```bash
   docker build -t embrapa-api .
   ```

2. Execute o contêiner:
   ```bash
   docker run -p 5000:5000 embrapa-api
   ```

## Testes

Execute os testes unitários com:

```bash
# Executa todos os testes
pytest

# Executa testes com cobertura
pytest --cov=app
```

## Validação de Código

Valide o código com:

```bash
# Verifica o estilo de código
flake8 app.py

# Formata o código
black app.py

# Verifica tipos
mypy app.py
```

## Uso da API

### Get Embrapa Data

**Endpoint:** `/embrapa_data`

**Method:** GET

**Query Parameters:**
- `ano` (optional): Year for which to retrieve data (default: 2023)

**Example:**
```
GET /embrapa_data?ano=2022
```

**Response:**
```json
[
    {
        "Produto": "Vinho de Mesa",
        "Quantidade (L.)": 123456789
    },
    {
        "Produto": "Espumante",
        "Quantidade (L.)": 98765432
    }
]
```

### Health Check

**Endpoint:** `/health`

**Method:** GET

**Response:**
```json
{
    "status": "healthy",
    "service": "embrapa-crawler"
}
```

## Development

### Testing

Run tests with pytest:
```bash
pytest
```

### Code Formatting

Format your code with Black:
```bash
black .
```

### Linting

Check your code with Flake8:
```bash
flake8
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
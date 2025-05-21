# Embrapa Data Crawler API

Uma API baseada em Flask para extrair e disponibilizar dados de produção e processamento de vinhos do site da Embrapa.

## Funcionalidades

- Web crawler para dados de produção de vinhos da Embrapa
- Web crawler para dados de processamento de vinhos da Embrapa
- Web crawler para dados de comercialização de vinhos da Embrapa
- Web crawler para dados de importação de vinhos da Embrapa
- Web crawler para dados de exportação de vinhos da Embrapa
- API RESTful com respostas em formato JSON
- Filtragem de dados por ano
- Diferentes formatos de resposta (padrão e hierárquico)
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

### Obter Dados de Produção

**Endpoint:** `/embrapa_data`

**Method:** GET

**Query Parameters:**
- `ano` (optional): Ano para o qual se deseja obter os dados (padrão: 2023)

**Example:**
```
GET /embrapa_data?ano=2022
```

**Response:**
```json
{
  "item 1": {
    "produto": "Vinhos de Mesa",
    "quantidade": 220249261,
    "subitem": [
      {
        "produto": "Tinto",
        "quantidade": 190099917
      },
      {
        "produto": "Branco",
        "quantidade": 27918722
      },
      {
        "produto": "Rosado",
        "quantidade": 2230622
      }
    ]
  },
  "item 2": {
    "produto": "Outros derivados",
    "quantidade": 7333215,
    "subitem": []
  },
  "total": 227582476
}
```

### Obter Dados de Processamento

**Endpoint:** `/embrapa_processamento`

**Method:** GET

**Query Parameters:**
- `ano` (optional): Ano para o qual se deseja obter os dados (padrão: 2023)
- `formato` (optional): Formato da resposta, pode ser "padrao" ou "hierarquico" (padrão: "padrao")

**Example:**
```
GET /embrapa_processamento?ano=2022&formato=hierarquico
```

**Response (formato hierárquico):**
```json
{
  "processos": {
    "Vinificação em Tinto": {
      "volume": 150000000,
      "subprocessos": [
        {
          "processo": "Tradicional",
          "volume": 120000000,
          "metodo": "Clássico"
        },
        {
          "processo": "Maceração Carbônica",
          "volume": 30000000,
          "metodo": "Especial"
        }
      ]
    },
    "Vinificação em Branco": {
      "volume": 50000000,
      "subprocessos": [
        {
          "processo": "Tradicional",
          "volume": 45000000,
          "metodo": "Padrão"
        },
        {
          "processo": "Com Maceração Pelicular",
          "volume": 5000000,
          "metodo": "Especial"
        }
      ]
    }
  },
  "totalGeral": 200000000
}
```

### Obter Dados de Comercialização

**Endpoint:** `/embrapa_comercializacao`

**Method:** GET

**Query Parameters:**
- `ano` (optional): Ano para o qual se deseja obter os dados (padrão: 2023)

**Example:**
```
GET /embrapa_comercializacao?ano=2022
```

**Response:**
```json
{
  "comercializacao": {
    "produto": "Vinhos de Mesa",
    "quantidade": 150000000,
    "mercados": [
      {
        "mercado": "Nacional",
        "quantidade": 120000000
      },
      {
        "mercado": "Internacional",
        "quantidade": 30000000
      }
    ]
  },
  "total": 150000000
}
```

### Obter Dados de Importação

**Endpoint:** `/embrapa_importacao`

**Method:** GET

**Query Parameters:**
- `ano` (optional): Ano para o qual se deseja obter os dados (padrão: 2023)
- `formato` (optional): Formato da resposta, pode ser "padrao" ou "hierarquico" (padrão: "padrao")
- `opcao` (optional): Opção de relatório (padrão: "opt_05")
- `subopcao` (optional): Subopção de relatório (padrão: "subopt_03")

**Example:**
```
GET /embrapa_importacao?ano=2022&formato=hierarquico
```

**Response (formato padrão):**
```json
{
  "importacao 1": {
    "pais": "Argentina",
    "quantidade": 8542125,
    "valor": 12567890.50
  },
  "importacao 2": {
    "pais": "Chile",
    "quantidade": 5236985,
    "valor": 9321567.75
  },
  "total_quantidade": 13779110,
  "total_valor": 21889458.25
}
```

**Response (formato hierárquico):**
```json
{
  "paises": {
    "Argentina": {
      "quantidade": 8542125,
      "valor": 12567890.50
    },
    "Chile": {
      "quantidade": 5236985,
      "valor": 9321567.75
    }
  },
  "totalGeral": {
    "quantidade": 13779110,
    "valor": 21889458.25
  }
}
```

### Obter Dados de Exportação

**Endpoint:** `/embrapa_exportacao`

**Method:** GET

**Query Parameters:**
- `ano` (optional): Ano para o qual se deseja obter os dados (padrão: 2023)
- `formato` (optional): Formato da resposta, pode ser "padrao" ou "hierarquico" (padrão: "padrao")
- `opcao` (optional): Opção de relatório (padrão: "opt_06")
- `subopcao` (optional): Subopção de relatório (padrão: "subopt_03")

**Example:**
```
GET /embrapa_exportacao?ano=2022&formato=hierarquico
```

**Response (formato padrão):**
```json
{
  "exportacao 1": {
    "pais": "Estados Unidos",
    "quantidade": 3254896,
    "valor": 7854692.30
  },
  "exportacao 2": {
    "pais": "Reino Unido",
    "quantidade": 1587452,
    "valor": 5321478.45
  },
  "total_quantidade": 4842348,
  "total_valor": 13176170.75
}
```

**Response (formato hierárquico):**
```json
{
  "paises": {
    "Estados Unidos": {
      "quantidade": 3254896,
      "valor": 7854692.30
    },
    "Reino Unido": {
      "quantidade": 1587452,
      "valor": 5321478.45
    }
  },
  "totalGeral": {
    "quantidade": 4842348,
    "valor": 13176170.75
  }
}
```

### Health Check

**Endpoint:** `/health`

**Method:** GET

**Response:**
```json
{
  "status": "online",
  "message": "API de dados da Embrapa está funcionando corretamente"
}
```

## Development

### Testing

Run tests with pytest:
```bash
# Executar todos os testes
pytest

# Executar apenas os testes de produção
pytest test_app.py

# Executar apenas os testes de processamento
pytest test_processamento.py
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

## Estrutura do Projeto

```
.
├── app.py                      # Ponto de entrada da aplicação
├── Dockerfile                  # Configuração para criação da imagem Docker
├── mypy.ini                    # Configuração para tipagem estática
├── README.md                   # Documentação do projeto
├── requirements.txt            # Dependências do projeto
├── run.sh                      # Script para execução em produção
├── test_app.py                 # Testes para a aplicação
├── test_processamento.py       # Testes para o processamento
└── src/                        # Código fonte da aplicação
    ├── __init__.py             # Inicializador do pacote
    ├── config/                 # Configurações da aplicação
    │   ├── __init__.py
    │   └── configuracao.py     # Variáveis de configuração
    ├── controllers/            # Controladores da aplicação
    │   ├── __init__.py
    │   ├── controlador_producao.py   # Controlador para dados de produção
    │   └── controlador_processamento.py # Controlador para dados de processamento
    ├── models/                 # Modelos de dados
    │   ├── __init__.py
    │   ├── producao.py         # Modelo para dados de produção
    │   └── processamento.py    # Modelo para dados de processamento
    ├── routes/                 # Rotas da API
    │   ├── __init__.py
    │   └── rotas.py            # Definição de endpoints
    ├── services/               # Serviços de negócio
    │   ├── __init__.py
    │   ├── servico_embrapa.py  # Serviço para obtenção de dados de produção
    │   └── servico_processamento.py # Serviço para obtenção de dados de processamento
    └── utils/                  # Utilitários
        └── __init__.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
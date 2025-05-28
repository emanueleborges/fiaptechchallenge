# 🍷 API Embrapa - Dados Vitivinícolas

Esta API extrai dados vitivinícolas do site oficial da Embrapa através de web scraping em tempo real. 

⚠️ **Importante:** A API depende da disponibilidade do site da Embrapa. Se o site estiver offline, você receberá uma mensagem de erro informando sobre a indisponibilidade.

---

## 🚀 Como usar

### Opção 1: Executar localmente

#### 1. Configurar variáveis de ambiente (opcional)
Copie o arquivo `.env.example` para `.env` e configure conforme necessário:
```bash
copy .env.example .env
```

#### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

#### 3. Executar a API
```bash
python app.py
```

✅ **API rodando em:** `http://localhost:5000`

### Opção 2: Executar com Docker

#### 1. Build e execução rápida
```bash
docker build -t embrapa-api .
docker run -p 5000:5000 embrapa-api
```

#### 2. Usando Docker Compose (recomendado)
```bash
# Produção
docker-compose up -d

# Desenvolvimento (com hot reload)
docker-compose --profile dev up -d api-dev
```

✅ **API rodando em:** `http://localhost:5000` (produção) ou `http://localhost:5001` (desenvolvimento)

---

## 📋 Endpoints disponíveis

### Status da API
```
GET /health
```
**Retorna:** Status de funcionamento da API

---

### Dados da Embrapa
```
GET /embrapa_data
```

**Parâmetros obrigatórios:**
- `ano` - Ano dos dados (ex: 2022)
- `opcao` - Tipo de dados:
  - `opt_02` = Produção
  - `opt_03` = Processamento  
  - `opt_04` = Comercialização
  - `opt_05` = Importação
  - `opt_06` = Exportação

---

## 🌊 Fluxo da Aplicação

O fluxo de funcionamento da aplicação é o seguinte:

1.  **Coleta de Dados:** Os dados são obtidos em tempo real do site da Embrapa utilizando técnicas de web scraping.
2.  **Disponibilização dos Dados:** A API retorna os dados coletados em formato JSON, prontos para serem consumidos por outras aplicações ou ferramentas de visualização.
3.  **Versionamento e CI/CD:** 
    *   O código-fonte é versionado no GitHub.
    *   Ao realizar um push para a branch `main` ou ao criar uma tag, uma pipeline do GitHub Actions é acionada.
4.  **Pipeline do GitHub Actions e Implantação:**
    *   A pipeline constrói a imagem Docker da aplicação.
    *   A imagem é enviada para o GitHub Container Registry (GHCR).
    *   Um deploy hook é acionado para atualizar a aplicação no Render.
5.  **Visualização/Acesso:** A API pode ser acessada e seus dados visualizados através do seguinte endereço: [https://fiaptechchallenge.onrender.com/](https://fiaptechchallenge.onrender.com/)

---

## 💡 Exemplos práticos

### Consultar produção de 2022
```
http://localhost:5000/embrapa_data?ano=2022&opcao=opt_02
```

### Consultar exportações de 2021
```
http://localhost:5000/embrapa_data?ano=2021&opcao=opt_06
```

**Resposta exemplo (sucesso):**
```json
{
  "ano": 2022,
  "opcao": "opt_02", 
  "dados": [
    {
      "produto": "VINHO DE MESA",
      "quantidade": "123456789"
    }
  ]
}
```

**Resposta exemplo (site offline):**
```json
{
  "erro": "Site da Embrapa está offline. Tente buscar dados via scrapers alternativos",
  "status": "site_offline"
}
```
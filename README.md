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
    - `subopcao`
      - `subopt_01`
      - `subopt_02`
      - `subopt_03`
      - `subopt_04`
  - `opt_04` = Comercialização
  - `opt_05` = Importação
    - `subopcao`
      - `subopt_01`
      - `subopt_02`
      - `subopt_03`
      - `subopt_04`
      - `subopt_05`
  - `opt_06` = Exportação
    - `subopcao`
      - `subopt_01`
      - `subopt_02`
      - `subopt_03`
      - `subopt_04`
---

## 💡 Exemplos práticos

### Consultar produção de 2022
```
http://localhost:5000/embrapa_data?ano=2022&opcao=opt_02
```

**Resposta exemplo (sucesso):**
```json
{
"Total": 457792870,
"itens": [
  {
    "produto": "VINHO DE MESA",
    "quantidade": 169762429,
    "subitem": [
        {
          "produto": "Tinto",
          "quantidade": 139320884
        },
        {
          "produto": "Branco",
          "quantidade": 27910299
        },
        {
          "produto": "Rosado",
          "quantidade": 2531246
        }
        ]
        },
        {
          "produto": "VINHO FINO DE MESA (VINIFERA)",
          "quantidade": 46268556,
          "subitem": [
        {
          "produto": "Tinto",
          "quantidade": 23615783
        },
        {
          "produto": "Branco",
          "quantidade": 20693437
        },
        {
          "produto": "Rosado",
          "quantidade": 1959336
        }
        ]
        },
```
### Consultar Processamento de 2023
```
http://localhost:5000/embrapa_data?ano=2023&opcao=opt_03&subopcao=subopt_02
```

**Resposta exemplo (sucesso):**
```json
{
"Total": 565243922,
"itens": [
    {
    "produto": "TINTAS",
    "quantidade": 502666358,
    "subitem": [
        {
          "produto": "Bacarina",
          "quantidade": 0
        },
        {
          "produto": "Bailey",
          "quantidade": 587066
        },
        {
        "produto": "Bordo",
        "quantidade": 154310837
        },
        {
          "produto": "Bourdin (S)",
          "quantidade": 0
        },
        {
          "produto": "BRS Carmen",
          "quantidade": 22242535
        },
        {
          "produto": "BRS Cora",
          "quantidade": 19508450
        },
        {
          "produto": "BRS Magna",
          "quantidade": 13919693
        },
        {
          "produto": "BRS Margot",
          "quantidade": 36842
        },
```

---

## 🏛️ Arquitetura e Fluxo de Implantação

A solução compreende as seguintes etapas principais:

1.  **Ingestão de Dados:** Extração em tempo real de dados vitivinícolas do [site da Embrapa](http://vitibrasil.cnpuv.embrapa.br/index.php) via web scraping pela API Python (Flask).
2.  **Processamento e API:** Os dados são estruturados em JSON e disponibilizados através de endpoints RESTful para consulta (Produção, Comercialização, etc.).
3.  **Versionamento:** O código é versionado no GitHub.
4.  **CI/CD com GitHub Actions:** Um workflow (`.github/workflows/main.yml`) automatiza o processo:
    *   **Acionadores:** Pushes na `main`, criação de tags e Pull Requests para `main`.
    *   **Principais Etapas:** Checkout do código, setup do Docker Buildx, login no GHCR, extração de metadados, build e push da imagem Docker para o GHCR (com cache), e acionamento de deploy hook no Render (para pushes na `main` via secret `RENDER_DEPLOY_HOOK_URL`).
5.  **Acesso à API:** Após o deploy, a API fica acessível em [https://fiaptechchallenge.onrender.com/](https://fiaptechchallenge.onrender.com/).

---

## 🍇 Cenário de Uso: Análise Preditiva para o Setor Vitivinícola

Esta API pode alimentar modelos de Machine Learning para gerar insights no setor vitivinícola.

**Objetivo:** Prever tendências de mercado, otimizar estoques e auxiliar decisões estratégicas usando dados históricos de produção, comercialização, importação e exportação.

**Solução Proposta (Visão Geral):**

1.  **Coleta e Armazenamento:** A API `fiaptechchallenge` fornece dados brutos. Um sistema robusto (Data Lake/Warehouse) armazenaria esses dados históricos, com processos ETL para limpeza e transformação.
2.  **Modelagem e Análise (ML):** Utilização de técnicas de EDA e modelos preditivos (séries temporais para demanda, regressão para otimização de produção) com ferramentas Python (Pandas, Scikit-learn, etc.).
3.  **Disponibilização de Insights:** Dashboards interativos (Power BI, Tableau, Dash/Streamlit) e alertas para apresentar resultados e previsões.

**Importância da API:** Atua como a fonte primária e confiável de dados da Embrapa, viabilizando a automação da coleta e garantindo que as análises sejam baseadas em informações consistentes e atualizadas.

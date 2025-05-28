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

---

## 🏛️ Arquitetura e Fluxo de Implantação

Esta seção detalha a arquitetura da solução, desde a coleta de dados até a implantação e acesso à API.

### 1. Ingestão de Dados
*   **Fonte:** Os dados vitivinícolas são extraídos em tempo real diretamente do [site oficial da Embrapa](http://vitibrasil.cnpuv.embrapa.br/index.php).
*   **Mecanismo:** A API Python (Flask) implementa a lógica de web scraping para coletar as informações conforme as requisições recebidas.

### 2. Processamento e Disponibilização via API
*   **Formato:** Os dados coletados são estruturados e retornados em formato JSON.
*   **Endpoints:** A API expõe endpoints específicos (detalhados na seção "Endpoints disponíveis") para consultar diferentes categorias de dados (Produção, Comercialização, Importação, Exportação) por ano.

### 3. Versionamento de Código
*   **Repositório:** Todo o código-fonte da aplicação é versionado utilizando Git e hospedado no GitHub.

### 4. Integração Contínua e Implantação Contínua (CI/CD) com GitHub Actions
O processo de CI/CD é automatizado utilizando GitHub Actions, com o workflow definido em `.github/workflows/main.yml`.
*   **Acionadores (Triggers):**
    *   Push de código para a branch `main`.
    *   Criação de tags (ex: `v1.0.0`, `v1.2.3`).
    *   Abertura ou atualização de Pull Requests para a branch `main`.
*   **Etapas do Workflow:**
    1.  **Checkout:** O código do repositório é baixado para o ambiente do GitHub Actions.
    2.  **Setup Docker Buildx:** O Docker Buildx é configurado para otimizar a construção de imagens multi-plataforma e melhorar o gerenciamento de cache.
    3.  **Login no GitHub Container Registry (GHCR):** Autenticação no GHCR utilizando um `GITHUB_TOKEN` (secret automático do GitHub) para permitir o push da imagem Docker.
    4.  **Extração de Metadados do Docker:** Tags e labels são gerados dinamicamente para a imagem Docker com base no evento que acionou o workflow (branch, tag, SHA do commit).
    5.  **Build e Push da Imagem Docker:**
        *   A aplicação Python é empacotada em uma imagem Docker.
        *   A imagem construída é enviada (push) para o GitHub Container Registry (GHCR), tornando-a disponível para implantação.
        *   O cache do GitHub Actions (`cache-from: type=gha`, `cache-to: type=gha,mode=max`) é utilizado para acelerar builds subsequentes.
    6.  **Implantação no Render (Deploy Hook):**
        *   Esta etapa ocorre **apenas** em pushes para a branch `main` e se o secret `RENDER_DEPLOY_HOOK_URL` estiver configurado no repositório.
        *   Um comando `curl` envia uma requisição POST para o *deploy hook* fornecido pelo Render.
        *   O Render, ao receber o sinal do hook, automaticamente baixa a imagem mais recente do GHCR e atualiza a aplicação em produção.

### 5. Acesso à API
*   Após a implantação bem-sucedida, a API fica publicamente acessível através da URL fornecida pelo Render: [https://fiaptechchallenge.onrender.com/](https://fiaptechchallenge.onrender.com/)
*   Os endpoints podem ser utilizados para obter os dados vitivinícolas, como exemplificado na seção "Exemplos práticos".

---

## 🍇 Cenário de Uso: Análise Preditiva para o Setor Vitivinícola

A API de dados da Embrapa pode ser uma ferramenta valiosa para alimentar modelos de análise e Machine Learning, visando gerar insights e previsões para o setor vitivinícola.

**Objetivo do Cenário:**
Desenvolver um sistema que utilize os dados históricos de produção, processamento, comercialização, importação e exportação de vinhos e derivados para prever tendências de mercado, otimizar estoques e auxiliar na tomada de decisão estratégica para produtores e distribuidores.

**Arquitetura da Solução Proposta (Além da API existente):**

1.  **Coleta Contínua de Dados:**
    *   A API `fiaptechchallenge` (esta API) serve como a principal fonte de dados brutos, sendo consultada periodicamente (ex: diariamente, semanalmente) por um script ou serviço agendado.

2.  **Armazenamento e Preparação de Dados:**
    *   **Data Lake/Warehouse:** Os dados JSON coletados da API seriam armazenados em um sistema de armazenamento mais robusto para dados históricos (ex: um Data Lake em S3/Azure Blob Storage, seguido por um Data Warehouse como BigQuery, Redshift ou Snowflake).
    *   **ETL (Extract, Transform, Load):** Processos de ETL seriam implementados para limpar, transformar (ex: converter tipos de dados, agregar por região/período) e carregar os dados no Data Warehouse, preparando-os para análise.

3.  **Modelagem e Análise (Machine Learning):**
    *   **Análise Exploratória de Dados (EDA):** Utilizar ferramentas como Jupyter Notebooks com Pandas, Matplotlib e Seaborn para explorar os dados históricos, identificar padrões, correlações e sazonalidades.
    *   **Desenvolvimento de Modelos Preditivos:**
        *   **Previsão de Demanda:** Modelos de séries temporais (ex: ARIMA, Prophet) poderiam ser treinados com dados de "Comercialização" e "Exportação" para prever a demanda futura de diferentes tipos de vinhos.
        *   **Otimização de Produção:** Modelos de regressão poderiam analisar como variações na "Produção" (tipo de uva, quantidade) impactam a "Comercialização" e os preços.
        *   **Análise de Sentimento (Complementar):** Se dados de notícias ou redes sociais sobre o setor fossem coletados, poderiam complementar a análise de tendências.
    *   **Ferramentas:** Python com bibliotecas como Scikit-learn, TensorFlow/Keras, XGBoost.

4.  **Disponibilização de Insights:**
    *   **Dashboards Interativos:** Os resultados das análises e as previsões dos modelos seriam apresentados em dashboards (ex: Power BI, Tableau, Google Data Studio, ou construídos com Dash/Streamlit em Python) para fácil interpretação por stakeholders.
    *   **Alertas:** Sistemas de alerta poderiam ser configurados para notificar sobre mudanças significativas nas tendências ou previsões.

**Como a API `fiaptechchallenge` é fundamental neste cenário:**
Ela atua como o **ponto de partida crucial e confiável**, fornecendo os dados primários da Embrapa de forma programática e estruturada. Sem essa API, a coleta de dados seria manual, propensa a erros e muito mais trabalhosa, inviabilizando a alimentação eficiente de um sistema de análise avançada como o descrito. A automação da coleta via API garante que os modelos e análises sejam baseados nos dados mais recentes e consistentes disponíveis.
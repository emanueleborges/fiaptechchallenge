# 🍷 API Embrapa - Dados Vitivinícolas

Esta API extrai dados vitivinícolas do site da Embrapa através de web scraping.

---

## 🚀 Como usar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar a API
```bash
python app.py
```

✅ **API rodando em:** `http://localhost:5001`

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

**Parâmetros opcionais:**
- `formato` - Formato dos dados (`padrao` ou `hierarquico`)
- `subopcao` - Filtro adicional por categoria

---

## 💡 Exemplos práticos

### Consultar produção de 2022
```
http://localhost:5001/embrapa_data?ano=2022&opcao=opt_02
```

### Consultar exportações de 2021 em formato hierárquico
```
http://localhost:5001/embrapa_data?ano=2021&opcao=opt_06&formato=hierarquico
```

**Resposta exemplo:**
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
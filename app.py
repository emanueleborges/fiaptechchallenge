import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from flask import Flask, request, Response
import re

app = Flask(__name__)

def crawl_embrapa(year):
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = []
    total_value = 0
    
    # Variável para armazenar categoria pai atual
    current_parent = None
    
    # Encontrar a tabela de dados (não todas as tabelas tb_base)
    tables = soup.find_all('table', class_='tb_base tb_dados')
    
    for table in tables:
        # Processar as linhas da tabela
        rows = table.find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2:
                # Extrair texto dos campos
                product = cols[0].text.strip()
                quantity_text = cols[1].text.strip()
                
                # Identificar se é um item pai (tb_item) ou filho (tb_subitem)
                is_parent = 'tb_item' in cols[0].get('class', [])
                
                # Se for Total, salvar o valor e continuar
                if product == 'Total':
                    total_text = quantity_text.replace('.', '').replace(',', '.')
                    try:
                        total_value = int(float(total_text))
                    except ValueError:
                        total_value = 0
                    continue
                
                # Se não for Total e não for cabeçalho "Produto"
                if product != 'Produto':
                    # Atualize o pai atual se for um item pai
                    if is_parent:
                        current_parent = product
                        parent_id = None
                    else:
                        parent_id = current_parent
                    
                    # Formatar valor numérico
                    if quantity_text == '-':
                        quantity = 0
                    else:
                        # Remove pontos dos números e substitui vírgulas por pontos
                        quantity = quantity_text.replace('.', '').replace(',', '.')
                        try:
                            # Tenta converter para número
                            quantity = int(float(quantity))
                        except ValueError:
                            quantity = 0
                    
                    # Adiciona o produto e sua quantidade aos dados
                    data.append({
                        'produto': product,
                        'quantidade': quantity,
                        'categoria_pai': parent_id,
                        'is_parent': is_parent
                    })
    
    # Adicionar Total como um item especial
    data.append({
        'produto': 'Total',
        'quantidade': total_value,
        'categoria_pai': None,
        'is_parent': True
    })
    
    # Cria o DataFrame com as colunas corretas
    df = pd.DataFrame(data)
    
    # Renomeia as colunas para o formato esperado
    df = df.rename(columns={
        'produto': 'Produto', 
        'quantidade': 'Quantidade (L.)', 
        'categoria_pai': 'Categoria_Pai'
    })
    
    return df

@app.route('/embrapa_data', methods=['GET'])
def get_embrapa_data():
    year = request.args.get('ano', default=2023, type=int)
    df_data = crawl_embrapa(year)
    
    # Estruturar os dados hierarquicamente
    produtos = []
    total = 0
    
    # Extrair o total
    total_row = df_data[df_data['Produto'] == 'Total']
    if not total_row.empty:
        total = total_row.iloc[0]['Quantidade (L.)']
        # Remover o Total do DataFrame para processamento
        df_data = df_data[df_data['Produto'] != 'Total']
    
    # Primeiro, processar os produtos pai (exceto "Dados da Vitivinicultura" e "DOWNLOAD")
    produtos_pai = df_data[(df_data['is_parent']) & 
                          (~df_data['Produto'].isin(['Dados da Vitivinicultura', 'DOWNLOAD']))]    # Criando a estrutura exata conforme solicitado
    resultado = {}
    produtos_dict = {}
    
    # Processar os produtos pai primeiro
    index = 1
    for _, row in produtos_pai.iterrows():
        nome_item = f"item {index}"
        produto_obj = {
            "produto": row['Produto'],
            "quantidade": row['Quantidade (L.)'],
            "subitem": []
        }
        resultado[nome_item] = produto_obj
        produtos_dict[row['Produto']] = produto_obj
        index += 1
    
    # Em seguida, processar os produtos filhos
    produtos_filhos = df_data[~df_data['is_parent']]
    for _, row in produtos_filhos.iterrows():
        categoria_pai = row['Categoria_Pai']
        # Verificar se o pai está no dicionário
        if categoria_pai in produtos_dict:
            produtos_dict[categoria_pai]['subitem'].append({
                "produto": row['Produto'],
                "quantidade": row['Quantidade (L.)']
            })
    
    # Adicionar o Total
    resultado["Total"] = int(total)
    
    # Função para converter tipos NumPy para tipos nativos Python
    def convert_numpy_types(obj):
        if hasattr(obj, 'item'):
            return obj.item()  # Converte numpy.int64, numpy.float64, etc. para Python int/float
        elif isinstance(obj, dict):
            return {k: convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(i) for i in obj]
        return obj
      # Converter todos os valores NumPy antes da serialização
    resultado = convert_numpy_types(resultado)
      # Reformatar o dicionário para o formato desejado com a sintaxe especial "item {"
    formato_final = {}
    items = {}
    
    # Primeiro, adicionar todos os itens com o formato correto
    for key, value in resultado.items():
        if key.startswith("item "):
            # Recolhemos todos os itens, vamos formatá-los depois
            items[key] = value
        elif key == "Total":
            formato_final["Total"] = value
            
    # Agora, formatamos os itens na ordem correta
    for i, (key, value) in enumerate(items.items(), 1):
        # Usar o formato especial "item {"
        formato_final[f"item {i} {{"] = value
    
    # Converter para JSON formatado
    json_output = json.dumps(formato_final, indent=4, ensure_ascii=False)
    return Response(json_output, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)

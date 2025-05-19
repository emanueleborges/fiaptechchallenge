# from flask import Flask
# from flask_jwt_extended import JWTManager
# from flask_restx import Api

# from src import config
# from src.controllers import api as vinho_ns

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(config.Config)

#     # JWT
#     JWTManager(app)

#     # RESTX (Swagger)
#     api = Api(
#         app,
#         version="1.0",
#         title="Vinho API (MVC)",
#         description="API simples em MVC para dados da Embrapa",
#         doc="/docs"
#     )
#     api.add_namespace(vinho_ns, path="/api")

#     return app

# if __name__ == "__main__":
#     app = create_app()
#     app.run(host="0.0.0.0", port=8000, debug=True)

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from flask import Flask, request, Response # Corrigido: Response importado

app = Flask(__name__) # Adicionado para inicializar o Flask

def crawl_embrapa(year):
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []
    tables = soup.find_all('table', class_='tb_base')

    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if len(cols) == 2 and cols[0] != 'Produto' and cols[0] != 'Total':
                product = cols[0]
                quantity = cols[1].replace('.', '').replace('-', '0') # Remove dots and replace '-' with 0
                try:
                    quantity = int(quantity)
                except ValueError:
                    quantity = 0 # if conversion fails, set to 0
                data.append([product, quantity])
    
    df = pd.DataFrame(data, columns=['Produto', 'Quantidade (L.)'])
    return df

@app.route('/embrapa_data', methods=['GET'])
def get_embrapa_data():
    year = request.args.get('ano', default=2023, type=int)
    df_data = crawl_embrapa(year)
    json_output = df_data.to_json(orient='records', indent=4, force_ascii=False)
    return Response(json_output, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)

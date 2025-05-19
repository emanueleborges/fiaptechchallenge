from flask import Blueprint
from controllers.services import crawl_embrapa
from flask import request, Response

routes = Blueprint('routes', __name__)

@routes.route('/embrapa_data', methods=['GET'])
def get_embrapa_data():
    year = request.args.get('ano', default=2023, type=int)
    df_data = crawl_embrapa(year)
    json_output = df_data.to_json(orient='records', indent=4, force_ascii=False)
    return Response(json_output, mimetype='application/json')
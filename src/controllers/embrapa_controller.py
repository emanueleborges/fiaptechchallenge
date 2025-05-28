
from flask import request, Response, jsonify
from src.services.embrapa_service import crawl_embrapa
from src.config.settings import logger

def get_embrapa_data_controller():
  
    try:
        year = request.args.get('ano', default=2023, type=int)
        logger.info(f"Received request for Embrapa data with year={year}")
        
        df_data = crawl_embrapa(year)
        json_output = df_data.to_json(orient='records', indent=4, force_ascii=False)
        
        return Response(json_output, mimetype='application/json')
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return jsonify({"error": "Failed to retrieve data", "details": str(e)}), 500

def health_check_controller():
   
    return jsonify({
        "status": "healthy",
        "service": "embrapa-crawler"
    })

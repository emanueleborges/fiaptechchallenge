#!/usr/bin/env python3
from flask import jsonify
from werkzeug.exceptions import HTTPException
from src.config.settings import logger

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        logger.error(f"HTTP error: {e}")
        return jsonify({"error": e.description}), e.code

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500

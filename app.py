import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from flask import Flask, request, Response
from src.config import Config
from src.controllers.routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)

from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required
)
from flask_restx import Namespace, Resource, fields

from src.models import authenticate
from src.services import fetch_opcao

api = Namespace("vinho", description="API de dados vitivinícolas")

login_model = api.model("Login", {
    "username": fields.String(required=True),
    "password": fields.String(required=True),
})

@api.route("/login")
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data = request.get_json()
        user = authenticate(data["username"], data["password"])
        if not user:
            return {"msg": "Credenciais inválidas"}, 401
        token = create_access_token(identity=user["username"])
        return {"access_token": token}

@api.route("/dados/<string:opcao>")
class Dados(Resource):
    @jwt_required()
    def get(self, opcao):
        """
        Retorna os dados brutos da Embrapa para a opção solicitada.
        """
        registros = fetch_opcao(opcao)
        return jsonify(registros)

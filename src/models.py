# Modelo simples de usuário fixo para autenticação
USERS = {
    "admin": {
        "username": "admin",
        "password": "senha"
    }
}

def authenticate(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        return {"username": user["username"]}
    return None

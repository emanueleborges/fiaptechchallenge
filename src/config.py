from datetime import timedelta

class Config:
    JWT_SECRET_KEY = "troque_por_uma_chave_secreta"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    RESTX_SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_VALIDATE = True
    RESTX_MASK_SWAGGER = False

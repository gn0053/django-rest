from rest_framework.authentication import TokenAuthentication as TokenAuth

class TokenAuthentication(TokenAuth):
    keyword = "Token"
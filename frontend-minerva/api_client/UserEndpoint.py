from api_client.client import ApiClient

class UserEndpoint:

    def __init__(self, client: ApiClient):
        self.client = client

    def create_user(self, data: dict):
        """POST /usuarios/register — cria um novo usuário"""
        return self.client.post("/usuarios/register", data=data)

    def update_user(self, data: dict):
        """PUT /usuarios/update/me — atualiza dados de um usuário"""
        return self.client.put(f"/usuarios/update/me", data=data)

    def delete_user(self):
        """DELETE /usuarios/me — remove um usuário"""
        return self.client.delete(f"/usuarios/me")

    def login(self, username: str, email: str, senha: str):
        """
        POST /login — faz login e configura o token JWT no cliente.
        """
        response = self.client.post("usuarios/login", data={"username": username, "email": email, "senha": senha})

        token = response.get("token")
        if not token:
            raise Exception("Token JWT não retornado pela API de login.")

        self.client.set_token(token)
        return token
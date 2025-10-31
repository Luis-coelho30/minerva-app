from api_client.client import ApiClient

class UserEndpoint:

    def __init__(self, client: ApiClient):
        self.client = client

    def create_user(self, data: dict):
        """POST /usuarios/register - cria um novo usuário"""
        return self.client.post("/usuarios/register", data=data)

    def update_user(self, data: dict):
        """PUT /usuarios/me - atualiza dados de um usuário"""
        return self.client.put(f"/usuarios/me", data=data)

    def delete_user(self):
        """DELETE /usuarios/me - remove um usuário"""
        return self.client.delete(f"/usuarios/me")

    def login(self, username: str, email: str, senha: str):
        """
        POST /login - faz login e salva o cookie JWT automaticamente via requests.Session
        """
        data = {"username": username, "email": email, "senha": senha}
        response = self.client.session.post(self.client._make_url("usuarios/login"), json=data)

        if response.status_code == 401:
            raise Exception("Credenciais inválidas")

        print("Cookies recebidos:", self.client.session.cookies.get_dict())
        return response.status_code
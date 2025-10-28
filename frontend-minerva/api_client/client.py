import requests

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.token = None
        self.headers = {"Content-Type": "application/json"}

    def _make_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def set_token(self, token: str):
        """Define o token JWT para futuras requisições."""
        self.token = token
        self.headers["Authorization"] = f"Bearer {token}" # Adiciona o token ao cabeçalho

    def clear_token(self):
        self.token = None
        self.headers.pop("Authorization", None)

    def _handle_response(self, response: requests.Response):
        if response.ok:
            try:
                return response.json()
            except ValueError:
                return response.text
        else:
            raise Exception(f"Erro {response.status_code}: {response.text}")

    def get(self, endpoint: str, params: dict | None = None):
        response = self.session.get(self._make_url(endpoint), headers=self.headers, params=params)
        return self._handle_response(response)

    def post(self, endpoint: str, data: dict | None = None):
        response = self.session.post(self._make_url(endpoint), headers=self.headers, json=data)
        return self._handle_response(response)

    def put(self, endpoint: str, data: dict | None = None):
        response = self.session.put(self._make_url(endpoint), headers=self.headers, json=data)
        return self._handle_response(response)

    def delete(self, endpoint: str):
        response = self.session.delete(self._make_url(endpoint), headers=self.headers)
        return self._handle_response(response)

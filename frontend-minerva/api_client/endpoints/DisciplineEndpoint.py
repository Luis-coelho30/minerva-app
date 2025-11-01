from api_client.client import ApiClient

class DisciplinaEndpoint:

    def __init__(self, client: ApiClient):
        self.client = client

    def list_user_discipline(self):
        """GET disciplinas/me - lista todas as disciplinas do usuário logado"""
        return self.client.get(f"disciplinas/me")
    
    def list_discipline_by_id(self, discId: int):
        """GET disciplinas/me/{discId} - lista disciplina por ID"""
        return self.client.get(f"disciplinas/me/{discId}")
    
    def create_discipline(self, data: dict):
        """POST disciplinas/me - cria uma nova disciplina para o usuário logado"""
        return self.client.post("disciplinas/me", data=data)
    
    def update_discipline(self, discId: int, data: dict):
        """PUT /disciplinas/me/{discId} - atualiza uma disciplina pelo ID"""
        return self.client.put(f"disciplinas/me/{discId}", data=data)
    
    def delete_discipline(self, discId: int):
        """DELETE /disciplinas/me/{discId} - apaga uma disciplina pelo ID"""
        return self.client.delete(f"disciplinas/me/{discId}")

from api_client.client import ApiClient

class DisciplinaEndpoint:

    def __init__(self, client: ApiClient):
        self.client = client

    def list_user_discipline(self):
        """GET disciplinas/me - lista todas as disciplinas do usuário logado"""
        return self.client.get(f"disciplinas/me")
    
    def list_discipline_by_id(self, userId: int):
        """GET disciplinas/me/{id} - lista disciplina por ID"""
        return self.client.get(f"disciplinas/me/{userId}")
    
    def create_discipline(self, nome: str, descricao: str, arquivada: bool, mediaNecessaria: float, creditos: int):
        """POST disciplinas/me - cria uma nova disciplina para o usuário logado"""
        return self.client.post(
            "disciplinas/me", 
            data={
            "nome": nome, 
            "descricao": descricao, 
            "arquivada": arquivada, 
            "mediaNecessaria": mediaNecessaria, 
            "creditos": creditos
            }
        )
    
    def update_discipline(self, userId: int, nome: str, descricao: str, arquivada: bool, mediaNecessaria: float, creditos: int):
        """PUT /disciplinas/me/{name} - atualiza uma disciplina pelo ID"""
        return self.client.put(
            f"disciplinas/me/{userId}", 
            data={
            "nome": nome, 
            "descricao": descricao, 
            "arquivada": arquivada, 
            "mediaNecessaria": mediaNecessaria, 
            "creditos": creditos
            }
        )
    
    def delete_discipline(self, userId: int):
        """DELETE /disciplinas/me/{name} - apaga uma disciplina pelo ID"""
        return self.client.delete(f"disciplinas/me/{userId}")

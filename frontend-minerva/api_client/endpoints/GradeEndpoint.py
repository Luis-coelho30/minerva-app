from api_client.client import ApiClient

class GradeEndpoint:

    def __init__(self, client: ApiClient):
        self.client = client

    def list_grades_by_discipline(self, discId: int):
        """GET /notas/me/{discId} - lista todas as notas de uma disciplina"""
        return self.client.get(f"notas/me/{discId}")
    
    def create_grade(self, descricao: str, valor: float, peso: int, disciplinaId: int):
        """POST /notas/me - cria uma nova nota para o usuário logado"""
        return self.client.post(
            "notas/me", 
            data={
            "descricao": descricao, 
            "valor": valor, 
            "peso": peso, 
            "disciplinaId": disciplinaId, 
            }
        )
    
    def update_grade(self, gradeId: int, descricao: str, valor: float, peso: int, disciplinaId: int):
        """PUT /notas/me/{gradeId} - atualiza uma nota pelo ID"""
        return self.client.put(
            f"notas/me/{gradeId}", 
            data={
            "descricao": descricao, 
            "valor": valor, 
            "peso": peso, 
            "disciplinaId": disciplinaId, 
            }
        )
    
    def delete_grade(self, gradeId: int):
        """DELETE /notas/me/{gradeId} - apaga uma nota pelo ID"""
        return self.client.delete(f"notas/me/{gradeId}")

from api_client.client import ApiClient

class GradeEndpoint:

    def __init__(self, client: ApiClient):
        self.client = client

    def list_grades_by_discipline(self, discId: int):
        """GET /notas/me/{discId} - lista todas as notas de uma disciplina"""
        return self.client.get(f"notas/me/disciplina/{discId}")

    def list_all_user_grades_grouped(self):
        """GET /notas/me/agrupadas - lista todas as notas de um usuário agrupadas por disciplina"""
        return self.client.get(f"notas/me/agrupadas")
    
    def create_grade(self, data: dict):
        """POST /notas/me - cria uma nova nota para o usuário logado"""
        return self.client.post("notas/me", data=data)
    
    def update_grade(self, gradeId: int, data: dict):
        """PUT /notas/me/{gradeId} - atualiza uma nota pelo ID"""
        return self.client.put(f"notas/me/{gradeId}", data=data)
    
    def delete_grade(self, gradeId: int):
        """DELETE /notas/me/{gradeId} - apaga uma nota pelo ID"""
        return self.client.delete(f"notas/me/{gradeId}")

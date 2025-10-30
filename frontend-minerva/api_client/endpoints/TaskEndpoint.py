from api_client.client import ApiClient

class TaskEndpoint:

    def __init__(self, client: ApiClient):
        self.client = client

    def list_user_tasks(self):
        """GET tarefas/me - lista todas as tarefas do usuário logado"""
        return self.client.get(f"tarefas/me")
    
    def list_tasks_by_disciplina(self, disciplinaId: int):
        """GET tarefas/me?disciplinaId={id} - lista todas as tarefas do usuário logado pelo ID da disciplina"""
        return self.client.get(f"tarefas/me?disciplinaId={disciplinaId}")
    
    def create_task(self, titulo: str, descricao: str, status: str, disciplinaId: int | None, dataInicio: str, dataFim: str, 
                    concluido_em: str, prioridade: str, arquivada: bool):
        """POST tarefas/me - cria uma nova tarefa para o usuário logado"""
        return self.client.post(
            "tarefas/me", 
            data={
            "titulo": titulo, 
            "descricao": descricao, 
            "status": status, 
            "disciplinaId": disciplinaId, 
            "dataInicio": dataInicio, 
            "dataFim": dataFim, 
            "concluido_em": concluido_em,
            "prioridade": prioridade, 
            "arquivada": arquivada
            }
        )
    
    def update_task(self, tarefaId: int, titulo: str, descricao: str, status: str, disciplinaId: int | None, 
                    dataInicio: str, dataFim: str, concluido_em: str, prioridade: str, arquivada: bool):
        """PUT /tarefas/me/{id} - atualiza uma tarefa pelo ID"""
        return self.client.put(
            f"tarefas/me/{tarefaId}", 
            data={
            "titulo": titulo, 
            "descricao": descricao, 
            "status": status, 
            "disciplinaId": disciplinaId, 
            "dataInicio": dataInicio, 
            "dataFim": dataFim, 
            "concluido_em": concluido_em,
            "prioridade": prioridade, 
            "arquivada": arquivada
            }
        )
    
    def delete_task(self, tarefaId: int):
        """DELETE /tarefas/me/{id} - apaga uma tarefa pelo ID"""
        return self.client.delete(f"tarefas/me/{tarefaId}")

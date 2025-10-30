from api_client.client import ApiClient

class FileEndpoint:

    def __init__(self, client: ApiClient):
        self.client = client

    def list_files(self):
        """GET /arquivos/me - lista todas os arquivos do usuario logado"""
        return self.client.get(f"arquivos/me")
    
    def list_files_by_discipline(self, discId: int):
        """GET /arquivos/me?disciplinaId={discId} - lista todas os arquivos de uma disciplina pelo ID"""
        return self.client.get(f"arquivos/me?disciplinaId={discId}")
    
    def create_file(self, disciplinaId: int, nomeOriginal: str, url: str, tipo: str):
        """POST /arquivos/me/create - cria um novo arquivo para o usuário logado"""
        return self.client.post(
            "arquivos/me/create", 
            data={
            "disciplinaId": disciplinaId, 
            "nomeOriginal": nomeOriginal, 
            "url": url, 
            "tipo": tipo, 
            }
        )
    
    def update_file(self, fileId: int, disciplinaId: int, nomeOriginal: str, url: str, tipo: str):
        """PUT /arquivos/me/{fileId} - atualiza um arquivo pelo ID"""
        return self.client.put(
            f"arquivos/me/{fileId}", 
            data={
            "disciplinaId": disciplinaId, 
            "nomeOriginal": nomeOriginal, 
            "url": url, 
            "tipo": tipo, 
            }
        )
    
    def delete_file(self, fileId: int):
        """DELETE /arquivos/me/{fileId} - apaga uma nota pelo ID"""
        return self.client.delete(f"arquivos/me/{fileId}")

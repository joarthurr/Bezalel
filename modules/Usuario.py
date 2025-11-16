from modules.Tentativa import Tentativa

class Usuario:
    def __init__(self, nome: str, email: str, matricula: str, tentativas: list[Tentativa]):
        self.nome = nome
        self.email = email
        self.matricula = matricula
        self.tentativas = tentativas

    """Adiciojna uma nova tentativa ao histórico do usuário."""
    def adicionar_tentativa(self, tentativa: Tentativa):
        pass
    
    """Retorna a lista de tentativa do usuário."""
    def obter_relatorio(self) -> list[Tentativa]:
        pass
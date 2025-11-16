from modules.Pergunta import Pergunta
from modules.Usuario import Usuario
from modules.Tentativa import Tentativa

class Quiz:
    def __init__(self, titulo: str, perguntas: list[Pergunta], tentativasLimite: int, tempoLimite: int):
        self.titulo = titulo
        self.perguntas = perguntas
        self.tentativasLimite = tentativasLimite
        self.tempoLimite = tempoLimite

    """Adiciona uma nova pergunta ao quiz."""
    def adicionar_pergunta(self, pergunta: Pergunta):
        pass

    """Calcula a pontuação máximo do quiz com base nos pesos."""
    def calcular_pontuacao_maxima(self) -> float:
        pass

    """Inicia uma nova tentativa para o usuário."""
    def iniciar_tentativa(self, usuario: Usuario) -> 'Tentativa':
        pass

    """Retorna uma representação em string do quiz."""
    def __str__(self) -> str:
        pass

    """Retorna o número de perguntas no quiz."""
    def __len__(self) -> int:
        pass

    """Permite iterar sobre as perguntas do quiz."""
    def __iter__(self):
        pass

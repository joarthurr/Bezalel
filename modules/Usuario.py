from __future__ import annotations
from typing import Dict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.Tentativa import Tentativa
    from modules.Quiz import Quiz

class Usuario:
    def __init__(self, nome: str, email: str, matricula: str, tentativas: list[Tentativa] = None):
        self.nome = nome
        self.email = email
        self.matricula = matricula
        self.tentativas = tentativas if tentativas is not None else []

    """Adiciona uma nova tentativa ao histórico do usuário."""
    def adicionar_tentativa(self, tentativa: Tentativa):
        self.tentativas.append(tentativa)
    
    """Retorna a lista de tentativa do usuário."""
    def obter_relatorio(self) -> list[Tentativa]:
        return self.tentativas.copy()
    
    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "email": self.email,
            "matricula": self.matricula,
            "tentativas": [t.to_dict() for t in self.tentativas]
        }

    @classmethod
    def from_dict(cls, data: dict, quizzes: Dict[str, Quiz] = None) -> Usuario:
        usuario = cls(
            nome=data["nome"],
            email=data["email"],
            matricula=data["matricula"]
        )
        
        if "tentativas" in data and quizzes:
            from modules.Tentativa import Tentativa
            for t_data in data["tentativas"]:
                titulo_quiz = t_data.get("quiz_titulo")
                if titulo_quiz in quizzes:
                    quiz = quizzes.get(titulo_quiz)
                    nova_tentativa = Tentativa.from_dict(t_data, usuario, quiz)
                    usuario.adicionar_tentativa(nova_tentativa)
        return usuario

from __future__ import annotations
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from modules.Tentativa import Tentativa
    from modules.Quiz import Quiz

class Usuario:
    def __init__(self, nome: str, email: str, matricula: str, tentativas: list[Tentativa] = None):
        self.nome = nome
        self.email = email
        self.matricula = matricula
        self.tentativas = tentativas if tentativas is not None else []

    def adicionar_tentativa(self, tentativa: Tentativa):
        """Adiciona uma nova tentativa ao histórico do usuário."""
        self.tentativas.append(tentativa)
    
    def obter_relatorio(self) -> list[Tentativa]:
        """Retorna uma cópia da lista de tentativas do usuário."""
        return self.tentativas.copy()

    def pode_realizar_quiz(self, quiz: Quiz) -> bool:
        """
        Verifica se o usuário ainda possui tentativas disponíveis para este quiz.
        Recebe o objeto Quiz para extrair o título e o limite internamente.
        """
        count = 0
        for t in self.tentativas:
            if t.quiz.titulo == quiz.titulo:
                count += 1
        
        return count < quiz.tentativasLimite

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
                
                if titulo_quiz and titulo_quiz in quizzes:
                    quiz = quizzes.get(titulo_quiz)
                    nova_tentativa = Tentativa.from_dict(t_data, usuario, quiz)
                    usuario.adicionar_tentativa(nova_tentativa)
        return usuario
    
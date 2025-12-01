from __future__ import annotations
import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from modules.Usuario import Usuario
    from modules.Quiz import Quiz

class Tentativa:
    def __init__(self, usuario: Usuario, quiz: Quiz, respostasDadas: list[int] = None, pontuacao: float = 0.0, tempoGasto: int = 0, dataInicio: datetime.datetime = None, dataFim: datetime.datetime = None, concluida: bool = None):
        self.usuario = usuario
        self.quiz = quiz
        self.respostasDadas = respostasDadas if respostasDadas is not None else []
        self.pontuacao = pontuacao
        self.tempoGasto = tempoGasto
        self.dataInicio = dataInicio if dataInicio else datetime.datetime.now()
        self.dataFim = dataFim
        self.concluida = False if concluida is None else concluida

    """Armazena a resposta dada pelo usuário para uma pergunta."""
    def registrar_resposta(self, indice_pergunta: int, indice_resposta: int):
        while len(self.respostasDadas) <= indice_pergunta:
            self.respostasDadas.append(-1)
        self.respostasDadas[indice_pergunta] = indice_resposta
    
    """Finaliza a tentativa calculando pontuação e tempo."""
    def finalizar(self):
        if self.concluida:
            return
        
        self.dataFim = datetime.datetime.now()
        tempoInt = self.dataFim - self.dataInicio
        self.tempoGasto = int(tempoInt.total_seconds())

        perguntas = self.quiz.perguntas
        totais = len(perguntas)
        
        if totais == 0:
            self.pontuacao = 0.0
        else:
            corretas = 0
            for i, pergunta in enumerate(perguntas):
                if i < len(self.respostasDadas):
                    indice_resposta_usuario = self.respostasDadas[i]
                    if indice_resposta_usuario != -1 and indice_resposta_usuario == pergunta.indiceCorreta:
                        corretas += 1
            self.pontuacao = (corretas / totais) * 100.0

        self.concluida = True
        self.usuario.adicionar_tentativa(self)

    def to_dict(self) -> dict:
        return {
            "quiz_titulo": self.quiz.titulo,
            "respostasDadas": self.respostasDadas,
            "pontuacao": self.pontuacao,
            "tempoGasto": self.tempoGasto,
            "dataInicio": self.dataInicio.isoformat(),
            "dataFim": self.dataFim.isoformat() if self.dataFim else None,
            "concluida": self.concluida
        }

    @classmethod
    def from_dict(cls, data: dict, usuario: Usuario, quiz: Quiz) -> Tentativa:
        return cls(
            usuario=usuario,
            quiz=quiz,
            respostasDadas=data["respostasDadas"],
            pontuacao=data["pontuacao"],
            tempoGasto=data["tempoGasto"],
            dataInicio=datetime.datetime.fromisoformat(data["dataInicio"]),
            dataFim=datetime.datetime.fromisoformat(data["dataFim"]) if data["dataFim"] else None,
            concluida=data["concluida"]
        )
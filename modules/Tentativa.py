from __future__ import annotations
import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.Usuario import Usuario
    from modules.Quiz import Quiz

PESOS = {"fácil": 1, "médio": 2, "difícil": 3, "FÁCIL": 1, "MÉDIO": 2, "DIFÍCIL": 3}
NOTA_CORTE = 70.0

class Tentativa:
    def __init__(self, usuario: Usuario, quiz: Quiz, respostasDadas: list[int] = None, pontuacao: float = 0.0, tempoGasto: int = 0, dataInicio: datetime.datetime = None, dataFim: datetime.datetime = None, concluida: bool = None):
        
        if dataInicio is None and not usuario.pode_realizar_quiz(quiz):
             raise ValueError(f"O limite de tentativas para o quiz '{quiz.titulo}' foi atingido.")

        self.usuario = usuario
        self.quiz = quiz
        self.respostasDadas = respostasDadas if respostasDadas is not None else []
        self.pontuacao = pontuacao
        self.tempoGasto = tempoGasto
        self.dataInicio = dataInicio if dataInicio else datetime.datetime.now()
        self.dataFim = dataFim
        self.concluida = False if concluida is None else concluida

    @property
    def aprovado(self) -> bool:
        """Verifica aprovação baseado na constante de configuração."""
        return self.pontuacao >= NOTA_CORTE

    def registrar_resposta(self, indice_pergunta: int, indice_resposta: int):
        """Armazena a resposta, bloqueando edições se a tentativa já acabou."""
        if self.concluida:
            raise ValueError("Não é possível alterar respostas de uma tentativa concluída.")
        
        while len(self.respostasDadas) <= indice_pergunta:
            self.respostasDadas.append(-1)
        self.respostasDadas[indice_pergunta] = indice_resposta
    
    def finalizar(self):
        """Calcula pontuação e tempo. Zera nota se estourar tempo."""
        if self.concluida:
            return
        
        self.dataFim = datetime.datetime.now()
        delta = self.dataFim - self.dataInicio
        self.tempoGasto = int(delta.total_seconds())
        
        tempo_limite_seg = self.quiz.tempoLimite * 60
        
        if self.tempoGasto > tempo_limite_seg:
            self.pontuacao = 0.0
        else:
            pontos_obtidos = 0
            pontos_totais_possiveis = 0
            
            for i, pergunta in enumerate(self.quiz.perguntas):
                peso = PESOS.get(pergunta.dificuldade, 1)
                pontos_totais_possiveis += peso

                if i < len(self.respostasDadas):
                    idx_resp = self.respostasDadas[i]
                    if idx_resp != -1 and idx_resp == pergunta.indiceCorreta:
                        pontos_obtidos += peso
            
            if pontos_totais_possiveis > 0:
                self.pontuacao = (pontos_obtidos / pontos_totais_possiveis) * 100.0
            else:
                self.pontuacao = 0.0

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
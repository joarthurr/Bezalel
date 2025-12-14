from __future__ import annotations
import datetime
from typing import TYPE_CHECKING
from config.config import Config

if TYPE_CHECKING:
    from modules.Usuario import Usuario
    from modules.Quiz import Quiz

class Tentativa:
    def __init__(self, usuario: Usuario, quiz: Quiz, respostasDadas: list[int] = None, pontuacao: float = 0.0, tempoGasto: int = 0, dataInicio: datetime.datetime = None, dataFim: datetime.datetime = None, concluida: bool = None, incompleta: bool = False):
        
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
        self.incompleta = incompleta
        self.encerradaPorTempo = False
        
        self._config = Config()

    @property
    def aprovado(self) -> bool:
        return self.pontuacao >= self._config.nota_corte

    def verificar_tempo_excedido(self) -> bool:
        agora = datetime.datetime.now()
        delta = agora - self.dataInicio
        tempo_decorrido_seg = int(delta.total_seconds())
        tempo_limite_seg = self.quiz.tempoLimite * 60
        return tempo_decorrido_seg > tempo_limite_seg

    def registrar_resposta(self, indice_pergunta: int, indice_resposta: int):
        if self.concluida:
            raise ValueError("Nao e possivel alterar respostas de uma tentativa concluida.")
        
        while len(self.respostasDadas) <= indice_pergunta:
            self.respostasDadas.append(-1)
        self.respostasDadas[indice_pergunta] = indice_resposta
    
    def finalizar(self):
        if self.concluida:
            return
        
        self.dataFim = datetime.datetime.now()
        delta = self.dataFim - self.dataInicio
        self.tempoGasto = int(delta.total_seconds())
        
        if self.verificar_tempo_excedido():
            self.pontuacao = 0.0
            self.incompleta = True
            self.encerradaPorTempo = True

        else:
            pontos_obtidos = 0
            pontos_totais_possiveis = 0
            
            for i, pergunta in enumerate(self.quiz.perguntas):
                peso = self._config.obter_peso(pergunta.dificuldade)
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
            "concluida": self.concluida,
            "incompleta": self.incompleta,
            "encerradaPorTempo": self.encerradaPorTempo,
        }

    @classmethod
    def from_dict(cls, data: dict, usuario: Usuario, quiz: Quiz) -> "Tentativa":
        tentativa = cls(
            usuario=usuario,
            quiz=quiz,
            respostasDadas=data["respostasDadas"],
            pontuacao=data["pontuacao"],
            tempoGasto=data["tempoGasto"],
            dataInicio=datetime.datetime.fromisoformat(data["dataInicio"]),
            dataFim=datetime.datetime.fromisoformat(data["dataFim"]) if data["dataFim"] else None,
            concluida=data["concluida"],
            incompleta=data.get("incompleta", False)
        )

        tentativa.encerradaPorTempo = data.get("encerradaPorTempo", False)
        return tentativa
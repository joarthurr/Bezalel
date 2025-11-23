from __future__ import annotations
import datetime

class Tentativa:
    def __init__(self, usuario: "Usuario", quiz: "Quiz", respostasDadas: list[str], pontuacao: float, tempoGasto: int, dataInicio: datetime, dataFim: datetime):
        self.usuario = usuario
        self.quiz = quiz
        self.respostasDadas = respostasDadas
        self.pontuacao = pontuacao
        self.tempoGasto = tempoGasto
        self.dataInicio = datetime.datetime.now()
        self.dataFim = dataFim
        self.concluida = False

    """Armazena a resposta dada pelo usuário para uma pergunta."""
    def registrar_resposta(self, resposta: str):
        pass
    
    """Finaliza a tentativa calculando pontuação e tempo."""
    def finalizar(self):
        pass
class Pergunta:
    def __init__(self, enunciado: str, alternativas: list[str], indiceCorreta: float, dificuldade: str, tema: str):
        self.enunciado = enunciado
        self.alternativas = alternativas
        self.indiceCorreta = indiceCorreta
        self.dificuldade = dificuldade
        self.tema = tema

    """Verifica se a resposta fornecida está correta."""
    def validar_resposta(self, resposta: str) -> bool:
        pass

    """Retorna uma representação em string da pergunta."""
    def __str__(self) -> str:
        pass

    """Compara duas perguntas com base no enunciado e alternativas."""
    def __eq__(self, other) -> bool:
        pass
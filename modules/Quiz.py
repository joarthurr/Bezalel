from modules.Pergunta import Pergunta

class Quiz:
    def __init__(self, titulo: str, perguntas: list[Pergunta] = None, tentativasLimite: int = 3, tempoLimite: int = 60):
        self.titulo = titulo
        self.perguntas = perguntas if perguntas is not None else []
        self.tentativasLimite = tentativasLimite
        self.tempoLimite = tempoLimite

    @property
    def titulo(self) -> str:
        return self._titulo
    
    @titulo.setter
    def titulo(self, valor: str):
        try:
            novo_titulo = valor.strip()
        except Exception:
            raise TypeError("O título deve ser um texto válido.")
        if not novo_titulo:
            raise ValueError("O título não pode ser vazio.")
        
        self._titulo = novo_titulo

    @property
    def perguntas(self) -> list[Pergunta]:
        return self._perguntas.copy()
    
    @perguntas.setter
    def perguntas(self, valor):
        try:
            lista_perguntas = list(valor)
        except TypeError:
            raise TypeError("As perguntas devem ser fornecidas em uma lista.")
        #if not lista_perguntas:
        #    raise ValueError("O quiz deve conter pelo menos uma pergunta.")
        
        for pergunta in lista_perguntas:
            if not (hasattr(pergunta, "enunciado") and hasattr(pergunta, "alternativas") and hasattr(pergunta, "indiceCorreta")):
                raise TypeError("Cada item da lista deve ser uma instância da classe Pergunta.")
            
        self._perguntas = lista_perguntas.copy()

    @property
    def tentativasLimite(self) -> int:
        return self._tentativasLimite
    
    @tentativasLimite.setter
    def tentativasLimite(self, valor: int):
        try:
            novo_limite = int(valor)
        except (TypeError, ValueError):
            raise TypeError("O limite de tentativas deve ser um número inteiro.")
        if novo_limite < 1:
            raise ValueError("O limite de tentativas deve ser pelo menos 1.")
        
        self._tentativasLimite = novo_limite

    @property
    def tempoLimite(self) -> int:
        return self._tempoLimite

    @tempoLimite.setter
    def tempoLimite(self, valor: int):
        try:
            novo_tempo = int(valor)
        except (TypeError, ValueError):
            raise TypeError("O limite de tempo deve ser um número inteiro.")
        if novo_tempo < 1:
            raise ValueError("O limite de tempo deve ser pelo menos 1 minuto.")
        
        self._tempoLimite = novo_tempo    

    def adicionar_pergunta(self, pergunta: Pergunta):
        if not (hasattr(pergunta, "enunciado") and hasattr(pergunta, "alternativas") and hasattr(pergunta, "indiceCorreta")):
            raise TypeError("O item deve ser uma instância da classe Pergunta.")
        self._perguntas.append(pergunta)

    def remover_pergunta(self, indice: int):
        try:
            del self._perguntas[indice]
        except (IndexError, TypeError):
            raise IndexError("Índice de pergunta inválido.")

    def __str__(self) -> str:
        return f"Quiz: {self.titulo} (Perguntas: {len(self.perguntas)})"

    def __len__(self) -> int:
        return len(self.perguntas)

    def __iter__(self):
        return iter(self._perguntas.copy())
    
    def __eq__(self, other) -> bool:
        try:
            return (self.titulo == other.titulo and
                    self.perguntas == other.perguntas)
        except AttributeError:
            return False

    def to_dict(self) -> dict:
        return {
            "titulo": self.titulo,
            "perguntas": [p.to_dict() for p in self.perguntas],
            "tentativasLimite": self.tentativasLimite,
            "tempoLimite": self.tempoLimite
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Quiz':
        perguntas_recuperadas = [Pergunta.from_dict(p) for p in data.get("perguntas", [])]
        return cls(
            titulo=data["titulo"],
            perguntas=perguntas_recuperadas,
            tentativasLimite=data.get("tentativasLimite", 3),
            tempoLimite=data.get("tempoLimite", 30)
        )
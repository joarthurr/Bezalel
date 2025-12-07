class Pergunta:
    def __init__(self, enunciado: str, alternativas: list[str], indiceCorreta: int, dificuldade: str, tema: str):
        self.enunciado = enunciado
        self.alternativas = alternativas
        self.indiceCorreta = indiceCorreta
        self.dificuldade = dificuldade
        self.tema = tema

    @property
    def enunciado(self) -> str:
        return self._enunciado
    
    @enunciado.setter
    def enunciado(self, valor: str):
        try:
            novo_enunciado = valor.strip()
        except Exception:
            raise TypeError("O enunciado deve ser um texto válido.")
        if not novo_enunciado:
            raise ValueError("O enunciado não pode ser vazio.")
        
        self._enunciado = novo_enunciado

    @property
    def alternativas(self) -> list[str]:
        return self._alternativas.copy()
    
    @alternativas.setter
    def alternativas(self, valor):
        try:
            lista_alts = list(valor)
        except TypeError:
            raise TypeError("As alternativas devem ser fornecidas em uma lista.")
        if not (3 <= len(lista_alts) <= 5):
            raise ValueError("A pergunta deve ter entre 3 e 5 alternativas.")
        
        novas_alts = []
        for alt in lista_alts:
            try:
                novas_alts.append(alt.strip())
            except AttributeError:
                raise TypeError("Cada alternativa deve ser um texto válido.")
            if alt.strip() == "":
                raise ValueError("Alternativas não podem ser vazias.")
        
        self._alternativas = novas_alts

    @property
    def indiceCorreta(self) -> int:
        return self._indiceCorreta
    
    @indiceCorreta.setter
    def indiceCorreta(self, valor):
        try:
            _ = self._alternativas[valor]
            self._indiceCorreta = valor
        except (IndexError, TypeError):
            raise ValueError("O índice da resposta correta é inválido.")

    @property
    def tema(self) -> str:
        return self._tema
    
    @tema.setter
    def tema(self, valor: str):
        try:
            novo_tema = valor.strip()
        except Exception:
            raise TypeError("O tema deve ser um texto válido.")
        if not novo_tema:
            raise ValueError("O tema não pode ser vazio.")
        
        self._tema = novo_tema

    @property
    def dificuldade(self) -> str:
        return self._dificuldade
    
    @dificuldade.setter
    def dificuldade(self, valor: str):
        dif_validas = {"fácil", "médio", "difícil"}
        try:
            novo_nivel = valor.strip().lower()
        except Exception:
            raise TypeError("A dificuldade deve ser um texto válido.")
        if novo_nivel not in dif_validas:
            raise ValueError(f"A dificuldade deve ser um dos seguintes níveis: {', '.join(dif_validas)}.")
        
        self._dificuldade = novo_nivel

    def __len__(self) -> int:
        return len(self.enunciado)

    def __str__(self) -> str:
        return f"Pergunta: {self.enunciado} (Tema: {self.tema}, Dificuldade: {self.dificuldade})"

    def __eq__(self, other) -> bool:
        try:
            return (self.enunciado == other.enunciado and
                    self.alternativas == other.alternativas and
                    self.indiceCorreta == other.indiceCorreta and
                    self.dificuldade == other.dificuldade and
                    self.tema == other.tema)
        except AttributeError:
            return False
        
    def to_dict(self):
        return {
        "enunciado": self.enunciado,
        "alternativas": self.alternativas,
        "indiceCorreta": self.indiceCorreta,
        "dificuldade": self.dificuldade,
        "tema": self.tema
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
        data["enunciado"],
        data["alternativas"],
        data["indiceCorreta"],
        data["dificuldade"],
        data["tema"]
        )

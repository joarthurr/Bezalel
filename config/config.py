import json
import os

CAMINHO_CONFIG = "settings.json"

class Config:
    _instance = None
    _dados = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._carregar()
        return cls._instance

    def _carregar(self):
        padrao = {
            "nota_corte_aprovacao": 70.0,
            "quiz_tempo_padrao_min": 10,
            "quiz_tentativas_padrao": 3,
            "pesos_dificuldade": {
                "fácil": 1, "médio": 2, "difícil": 3,
                "facil": 1, "medio": 2, "dificil": 3
            }
        }
        
        if not os.path.exists(CAMINHO_CONFIG):
            self._dados = padrao
            return

        try:
            with open(CAMINHO_CONFIG, "r", encoding="utf-8") as f:
                carregado = json.load(f)
                self._dados = {**padrao, **carregado}
        except Exception:
            self._dados = padrao

    @property
    def nota_corte(self) -> float:
        return float(self._dados.get("nota_corte_aprovacao", 70.0))

    @property
    def tempo_padrao(self) -> int:
        return int(self._dados.get("quiz_tempo_padrao_min", 10))
    
    @property
    def tentativas_padrao(self) -> int:
        return int(self._dados.get("quiz_tentativas_padrao", 3))

    def obter_peso(self, dificuldade: str) -> int:
        chave = dificuldade.lower()
        pesos = self._dados.get("pesos_dificuldade", {})
        return pesos.get(chave, 1)
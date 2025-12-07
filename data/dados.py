import json
import os
from modules.Usuario import Usuario
from modules.Quiz import Quiz

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_DB = os.path.join(DIRETORIO_ATUAL, "relatorio.json")

def salvar_dados(usuarios: list[Usuario], quizzes: list[Quiz]):
    dados = {
        "quizzes": [q.to_dict() for q in quizzes],
        "usuarios": [u.to_dict() for u in usuarios]
    }
    
    try:

        os.makedirs(os.path.dirname(ARQUIVO_DB), exist_ok=True)
        
        with open(ARQUIVO_DB, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print("Dados salvos com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar: {e}")

def carregar_dados() -> tuple[list[Usuario], list[Quiz]]:
    if not os.path.exists(ARQUIVO_DB):
        return [], []

    try:
        with open(ARQUIVO_DB, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return [], []

    quizzes_lista = []
    quizzes_map = {}
    
    for q_data in data.get("quizzes", []):
        try:
            quiz = Quiz.from_dict(q_data)
            quizzes_lista.append(quiz)
            quizzes_map[quiz.titulo] = quiz
        except Exception as e:
            print(f"Erro ao carregar quiz: {e}")

    usuarios_lista = []
    for u_data in data.get("usuarios", []):
        try:
            user = Usuario.from_dict(u_data, quizzes=quizzes_map)
            usuarios_lista.append(user)
        except Exception as e:
            print(f"Erro ao carregar usuário: {e}")

    return usuarios_lista, quizzes_lista
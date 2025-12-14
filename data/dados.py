import json
import os
from modules.Usuario import Usuario
from modules.Quiz import Quiz
from modules.Pergunta import Pergunta
from modules.Tentativa import Tentativa

ARQUIVO_DB = os.path.join("data", "db.json")

def salvar_dados(usuarios: list[Usuario], quizzes: list[Quiz]):
    data = {
        "usuarios": [u.to_dict() for u in usuarios],
        "quizzes": [q.to_dict() for q in quizzes]
    }
    
    os.makedirs(os.path.dirname(ARQUIVO_DB), exist_ok=True)
    
    with open(ARQUIVO_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Dados salvos com sucesso.")

def carregar_dados() -> tuple[list[Usuario], list[Quiz]]:
    if not os.path.exists(ARQUIVO_DB):
        return [], []

    try:
        with open(ARQUIVO_DB, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return [], []

    quizzes = []
    quizzes_dict = {}
    
    for q_data in data.get("quizzes", []):
        try:
            quiz = Quiz.from_dict(q_data)
            quizzes.append(quiz)
            quizzes_dict[quiz.titulo] = quiz
        except Exception as e:
            print(f"Erro ao carregar quiz: {e}")

    usuarios = []
    for u_data in data.get("usuarios", []):
        try:
            usuario = Usuario.from_dict(u_data)
            
            tentativas_reais = []
            for t_data in u_data.get("tentativas", []):
                titulo_quiz = t_data.get("quiz_titulo")
                if titulo_quiz in quizzes_dict:
                    quiz_ref = quizzes_dict[titulo_quiz]
                    try:
                        tentativa = Tentativa.from_dict(t_data, usuario, quiz_ref)
                        tentativas_reais.append(tentativa)
                    except Exception as e:
                        print(f"Erro ao carregar tentativa: {e}")
            
            usuario.tentativas = tentativas_reais
            usuarios.append(usuario)
        except Exception as e:
            print(f"Erro ao carregar usuario: {e}")

    return usuarios, quizzes
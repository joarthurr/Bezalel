import os
import pytest
from modules.Usuario import Usuario
from modules.Quiz import Quiz
from data.dados import salvar_dados, carregar_dados, ARQUIVO_DB

@pytest.fixture
def setup_banco():
    if os.path.exists(ARQUIVO_DB):
        os.remove(ARQUIVO_DB)
    yield
    if os.path.exists(ARQUIVO_DB):
        os.remove(ARQUIVO_DB)

def test_salvar_e_carregar_fluxo_completo(setup_banco):
    quiz = Quiz("Quiz Teste")
    user = Usuario("Tester", "test@email.com", "123")
    
    salvar_dados([user], [quiz])
    
    assert os.path.exists(ARQUIVO_DB)
    
    users_carregados, quizzes_carregados = carregar_dados()
    
    assert len(users_carregados) == 1
    assert len(quizzes_carregados) == 1
    assert users_carregados[0].nome == "Tester"
    assert quizzes_carregados[0].titulo == "Quiz Teste"
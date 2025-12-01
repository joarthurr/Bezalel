import pytest
from modules.Quiz import Quiz
from modules.Pergunta import Pergunta


def criar_pergunta():
    return Pergunta(
        "Qual a capital do Brasil?",
        ["Brasília", "Rio", "SP"],
        0,
        "fácil",
        "Geografia"
    )


def test_criacao_quiz_valido():
    p = criar_pergunta()
    q = Quiz("Meu Quiz", [p], 3, 60)

    assert q.titulo == "Meu Quiz"
    assert len(q) == 1
    assert q.tentativasLimite == 3
    assert q.tempoLimite == 60


def test_titulo_vazio_falha():
    p = criar_pergunta()
    with pytest.raises(ValueError):
        Quiz("", [p], 3, 60)


def test_quiz_pode_iniciar_vazio():
    """
    Teste ajustado: Agora é PERMITIDO criar um quiz com lista vazia.
    Isso é necessário para o carregamento do banco de dados e criação incremental.
    """
    q = Quiz("Quiz Vazio", [], 3, 60)
    assert len(q) == 0
    assert q.perguntas == []


def test_adicionar_pergunta():
    p1 = criar_pergunta()
    p2 = criar_pergunta()
    q = Quiz("Teste", [p1], 3, 60)

    q.adicionar_pergunta(p2)

    assert len(q) == 2


def test_remover_pergunta():
    p1 = criar_pergunta()
    q = Quiz("Teste", [p1], 3, 60)

    q.remover_pergunta(0)

    assert len(q) == 0


def test_iterador():
    p1 = criar_pergunta()
    p2 = criar_pergunta()
    q = Quiz("Teste", [p1, p2], 3, 60)

    perguntas = list(iter(q))

    assert perguntas[0].enunciado == p1.enunciado
    assert perguntas[1].enunciado == p2.enunciado


def test_validacao_tentativas_e_tempo():
    p1 = criar_pergunta()

    with pytest.raises(ValueError):
        Quiz("Quiz", [p1], -1, 60)

    with pytest.raises(ValueError):
        Quiz("Quiz", [p1], 3, -10)

    with pytest.raises(TypeError):
        Quiz("Quiz", [p1], "três", 60)

    with pytest.raises(TypeError):
        Quiz("Quiz", [p1], 3, "um minuto")
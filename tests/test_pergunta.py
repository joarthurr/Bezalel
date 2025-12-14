import pytest
from modules.Pergunta import Pergunta


def test_criacao_pergunta_valida():
    p = Pergunta(
        enunciado="Qual a capital da França?",
        alternativas=["Paris", "Budapeste", "Sofia"],
        indiceCorreta=0,
        dificuldade="fácil",
        tema="Geografia"
    )
    assert p.enunciado == "Qual a capital da França?"
    assert p.alternativas == ["Paris", "Budapeste", "Sofia"]
    assert p.indiceCorreta == 0
    assert p.dificuldade == "fácil"
    assert p.tema == "Geografia"


def test_enunciado_vazio_deve_falhar():
    with pytest.raises(ValueError):
        Pergunta("", ["a", "b", "c"], 0, "fácil", "tema")


def test_alternativas_invalidas():
    with pytest.raises(ValueError):
        Pergunta("Pergunta?", ["a", "b"], 0, "fácil", "tema")

    with pytest.raises(ValueError):
        Pergunta("Pergunta?", ["a", "b", "c", "d", "e", "f"], 0, "fácil", "tema")


def test_indice_correto_invalido():
    with pytest.raises(ValueError):
        Pergunta("Pergunta?", ["a", "b", "c"], 5, "fácil", "tema")


def test_dificuldade_invalida():
    with pytest.raises(ValueError):
        Pergunta("Pergunta?", ["a", "b", "c"], 0, "hard", "tema")


def test_len_retorna_tamanho_enunciado():
    p = Pergunta("ABC", ["x", "y", "z"], 0, "fácil", "tema")
    assert len(p) == 3


def test_str():
    p = Pergunta("Teste", ["a", "b", "c"], 1, "fácil", "tema")
    texto = str(p)
    assert "Teste" in texto
    assert "tema" in texto
    assert "fácil" in texto


def test_eq():
    p1 = Pergunta("Pergunta?", ["a", "b", "c"], 0, "médio", "tema")
    p2 = Pergunta("Pergunta?", ["a", "b", "c"], 0, "médio", "tema")
    assert p1 == p2

    p3 = Pergunta("Outra", ["a", "b", "c"], 0, "médio", "tema")
    assert p1 != p3
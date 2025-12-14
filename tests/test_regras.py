import pytest
import os
import json
from datetime import datetime, timedelta
from modules.Usuario import Usuario
from modules.Quiz import Quiz
from modules.Pergunta import Pergunta
from modules.Tentativa import Tentativa
from modules.Relatorio import Relatorio
from data.dados import salvar_dados, carregar_dados, ARQUIVO_DB

# --- FIXTURES (Dados prontos para os testes) ---
@pytest.fixture
def p_facil():
    return Pergunta("Q1", ["A", "B", "C"], 0, "fácil", "Matemática")

@pytest.fixture
def p_medio():
    return Pergunta("Q2", ["A", "B", "C"], 0, "médio", "História")

@pytest.fixture
def p_dificil():
    return Pergunta("Q3", ["A", "B", "C"], 0, "difícil", "Matemática")

@pytest.fixture
def quiz_padrao(p_facil, p_medio, p_dificil):
    return Quiz("Quiz Teste", [p_facil, p_medio, p_dificil], tentativasLimite=2, tempoLimite=10)

@pytest.fixture
def usuario_padrao():
    return Usuario("Tester", "t@t.com", "123")

# --- BLOCO 1: Validação de Perguntas (3 testes) ---

def test_criacao_pergunta_valida(p_facil):
    assert p_facil.dificuldade == "fácil"
    assert len(p_facil.alternativas) == 3

def test_erro_alternativas_insuficientes():
    with pytest.raises(ValueError):
        Pergunta("Q", ["A", "B"], 0, "fácil", "T")

def test_erro_indice_invalido():
    with pytest.raises(ValueError):
        Pergunta("Q", ["A", "B", "C"], 5, "fácil", "T")

# --- BLOCO 2: Cálculo de Pontuação (3 testes) ---

def test_pontuacao_maxima_ponderada(usuario_padrao, quiz_padrao):
    t = Tentativa(usuario_padrao, quiz_padrao)
    t.registrar_resposta(0, 0)
    t.registrar_resposta(1, 0)
    t.registrar_resposta(2, 0)
    t.finalizar()
    assert t.pontuacao == 100.0
    assert t.aprovado is True

def test_pontuacao_parcial_ponderada(usuario_padrao, quiz_padrao):
    t = Tentativa(usuario_padrao, quiz_padrao)
    t.registrar_resposta(0, 0)
    t.registrar_resposta(1, 0)
    t.registrar_resposta(2, 1)
    t.finalizar()
    assert t.pontuacao == 50.0

def test_pontuacao_zero(usuario_padrao, quiz_padrao):
    t = Tentativa(usuario_padrao, quiz_padrao)
    t.registrar_resposta(0, 1); t.registrar_resposta(1, 1); t.registrar_resposta(2, 1)
    t.finalizar()
    assert t.pontuacao == 0.0

# --- BLOCO 3: Tempo Limite (2 testes) ---

def test_tempo_excedido_zera_nota_e_marca_incompleta(usuario_padrao, quiz_padrao):
    t = Tentativa(usuario_padrao, quiz_padrao)
    t.dataInicio = datetime.now() - timedelta(minutes=20)
    
    t.finalizar()
    
    assert t.pontuacao == 0.0
    assert t.incompleta is True
    assert t.encerradaPorTempo is True

def test_verificacao_tempo_real(usuario_padrao, quiz_padrao):
    t = Tentativa(usuario_padrao, quiz_padrao)
    t.dataInicio = datetime.now() - timedelta(minutes=11)
    assert t.verificar_tempo_excedido() is True

# --- BLOCO 4: Limite de Tentativas (2 testes) ---

def test_usuario_pode_fazer_quiz(usuario_padrao, quiz_padrao):
    assert usuario_padrao.pode_realizar_quiz(quiz_padrao) is True

def test_bloqueio_apos_limite_atingido(usuario_padrao, quiz_padrao):
    t1 = Tentativa(usuario_padrao, quiz_padrao); t1.finalizar()
    t2 = Tentativa(usuario_padrao, quiz_padrao); t2.finalizar()
    
    assert usuario_padrao.pode_realizar_quiz(quiz_padrao) is False
    
    with pytest.raises(ValueError, match="limite de tentativas"):
        Tentativa(usuario_padrao, quiz_padrao)

# --- BLOCO 5: Relatórios e Filtros (4 testes) ---

def test_ranking_ignora_tentativa_tempo_excedido(usuario_padrao, quiz_padrao, capsys):
    t = Tentativa(usuario_padrao, quiz_padrao)
    t.dataInicio = datetime.now() - timedelta(minutes=20)
    t.finalizar()
    
    rel = Relatorio([usuario_padrao])
    rel.gerar_ranking()
    
    captured = capsys.readouterr()
    assert "Nenhum dado de desempenho" in captured.out or "valida" in captured.out

def test_ranking_considera_tentativa_valida(usuario_padrao, quiz_padrao, capsys):
    t = Tentativa(usuario_padrao, quiz_padrao)
    t.registrar_resposta(0, 0); t.registrar_resposta(1, 0); t.registrar_resposta(2, 0)
    t.finalizar()
    
    rel = Relatorio([usuario_padrao])
    rel.gerar_ranking()
    
    captured = capsys.readouterr()
    assert "100.00" in captured.out

def test_estatisticas_tema_filtra_incompletas(usuario_padrao, quiz_padrao, capsys):
    t1 = Tentativa(usuario_padrao, quiz_padrao)
    t1.registrar_resposta(0, 0)
    t1.finalizar()
    
    t2 = Tentativa(usuario_padrao, quiz_padrao)
    t2.dataInicio = datetime.now() - timedelta(minutes=20)
    t2.finalizar()
    
    rel = Relatorio([usuario_padrao])
    rel.gerar_desempenho_por_tema()
    
    captured = capsys.readouterr()
    assert "MATEMÁTICA" in captured.out

def test_distribuicao_notas(usuario_padrao, quiz_padrao, capsys):
    t = Tentativa(usuario_padrao, quiz_padrao)
    t.registrar_resposta(0, 0); t.registrar_resposta(1, 0); t.registrar_resposta(2, 0)
    t.finalizar()
    
    rel = Relatorio([usuario_padrao])
    rel.gerar_distribuicao_notas()
    
    captured = capsys.readouterr()
    assert "90-100" in captured.out

def test_taxa_global_calculo(usuario_padrao, quiz_padrao, capsys):
    t = Tentativa(usuario_padrao, quiz_padrao)
    t.registrar_resposta(0, 0)
    t.registrar_resposta(1, 1)
    t.finalizar()
    
    rel = Relatorio([usuario_padrao])
    rel.gerar_taxa_acerto_global()
    
    captured = capsys.readouterr()
    assert "50.00%" in captured.out

# --- BLOCO 6: Persistência (3 testes) ---

def test_persist_usuario(usuario_padrao, quiz_padrao):
    t = Tentativa(usuario_padrao, quiz_padrao)
    t.incompleta = True
    d = t.to_dict()
    assert d['incompleta'] is True

def test_salvar_carregar_fluxo(tmp_path, usuario_padrao, quiz_padrao):
    import data.dados
    arquivo_orig = data.dados.ARQUIVO_DB
    data.dados.ARQUIVO_DB = str(tmp_path / "test.json")
    
    try:
        t = Tentativa(usuario_padrao, quiz_padrao)
        t.finalizar()
        salvar_dados([usuario_padrao], [quiz_padrao])
        
        us, qs = carregar_dados()
        assert len(us) == 1
        assert us[0].tentativas[0].pontuacao == t.pontuacao
    finally:
        data.dados.ARQUIVO_DB = arquivo_orig
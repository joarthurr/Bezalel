import os
import time
from data.dados import carregar_dados, salvar_dados
from modules.Relatorio import Relatorio
from modules.Tentativa import Tentativa
from modules.Usuario import Usuario
from modules.Quiz import Quiz
from modules.Pergunta import Pergunta

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPressione ENTER para continuar...")

def ler_inteiro(mensagem: str):
    """Lê um número inteiro de forma segura."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

def menu_principal():
    limpar_tela()
    print("="*30)
    print("   Sistema de Quiz Educacional - Bezalel   ")
    print("="*30)
    print("1. Área do Aluno (Responder)")
    print("2. Área Administrativa")
    print("0. Sair e Salvar")
    return input("\nEscolha uma opção: ")

def menu_admin():
    limpar_tela()
    print("--- Menu Admin ---")
    print("1. Relatório de Alunos")
    print("2. Cadastrar Novo Usuário")
    print("3. Criar Novo Quiz")
    print("4. Adicionar Pergunta a Quiz Existente")
    print("5. Gerar Dados de Teste (Seed)")
    print("0. Voltar")
    return input("\nEscolha uma opção: ")

def criar_usuario_interativo(usuarios: list[Usuario]):
    print("\n--- Cadastro de Usuário ---")
    nome = input("Nome completo: ").strip()
    email = input("E-mail: ").strip()
    matricula = input("Matrícula: ").strip()
    
    if not nome or not email or not matricula:
        print("Todos os campos são obrigatórios.")
        pausar()
        return

    if any(u.matricula == matricula for u in usuarios):
        print(f"Já existe um usuário com a matrícula {matricula}.")
        pausar()
        return

    novo_user = Usuario(nome, email, matricula)
    usuarios.append(novo_user)
    print(f"Usuário {nome} cadastrado com sucesso!")
    pausar()

def criar_pergunta_interativa() -> Pergunta:
    """Fluxo passo-a-passo para criar uma pergunta."""
    print("\n--- Nova Pergunta ---")
    enunciado = input("Enunciado da questão: ").strip()
    tema = input("Tema (ex: Matemática, História): ").strip()
    
    print("Dificuldade (FÁCIL, MÉDIO, DIFÍCIL):")
    dificuldade = input(">> ").strip().upper()
    
    print("\nCadastre as alternativas (Mínimo 3, Máximo 5).")
    print("Deixe vazio e tecle ENTER para parar de adicionar.")
    alternativas = []
    while len(alternativas) < 5:
        alt = input(f"Alternativa {len(alternativas)}: ").strip()
        if not alt:
            if len(alternativas) >= 3:
                break
            else:
                print("Mínimo de 3 alternativas necessárias.")
                continue
        alternativas.append(alt)
    
    print("\nQual é a alternativa correta?")
    for i, alt in enumerate(alternativas):
        print(f"[{i}] {alt}")
    
    while True:
        idx = ler_inteiro("Índice da correta: ")
        if 0 <= idx < len(alternativas):
            break
        print("Índice inválido.")

    return Pergunta(enunciado, alternativas, idx, dificuldade, tema)

def criar_quiz_interativo(quizzes: list[Quiz]):
    print("\n--- Criação de Quiz ---")
    titulo = input("Título do Quiz: ").strip()
    
    tentativas = ler_inteiro("Limite de tentativas: ")
    tempo = ler_inteiro("Tempo limite (minutos): ")
    
    try:
        novo_quiz = Quiz(titulo, [], tentativas, tempo)
    except ValueError as e:
        print(f"Erro ao criar quiz: {e}")
        pausar()
        return

    print("\nAgora vamos adicionar perguntas.")
    while True:
        add = input("Deseja adicionar uma pergunta agora? (S/N): ").upper()
        if add != 'S':
            break
        
        try:
            pergunta = criar_pergunta_interativa()
            novo_quiz.adicionar_pergunta(pergunta)
            print("Pergunta adicionada!")
        except Exception as e:
            print(f"Erro ao adicionar pergunta: {e}")
    
    quizzes.append(novo_quiz)
    
    pausar()

def adicionar_pergunta_a_quiz_existente(quizzes: list[Quiz]):
    if not quizzes_check(quizzes): return
    
    print("\n--- Editar Quiz Existente ---")
    for i, q in enumerate(quizzes):
        print(f"{i}. {q.titulo} ({len(q)} questões)")
    
    try:
        idx = ler_inteiro("Escolha o Quiz para editar: ")
        quiz = quizzes[idx]
    except IndexError:
        print("Quiz inválido.")
        pausar()
        return

    try:
        pergunta = criar_pergunta_interativa()
        quiz.adicionar_pergunta(pergunta)
        print(f"Pergunta adicionada ao quiz '{quiz.titulo}'!")
    except Exception as e:
        print(f"Erro: {e}")
    pausar()

def fluxo_responder_quiz(usuarios: list[Usuario], quizzes: list[Quiz]):
    limpar_tela()
    if not users_check(usuarios) or not quizzes_check(quizzes): 
        pausar()
        return

    print("--- Área do Aluno ---")
    print("Quem é você?")
    for i, u in enumerate(usuarios):
        print(f"{i}. {u.nome} ({u.matricula})")
    
    try:
        idx_user = ler_inteiro("Seu número: ")
        usuario = usuarios[idx_user]
    except IndexError:
        print("Usuário inválido.")
        pausar()
        return

    print(f"\nBem-vindo(a), {usuario.nome}!")
    print("Quizzes disponíveis:")
    for i, q in enumerate(quizzes):
        print(f"{i}. {q.titulo} | {q.tempoLimite} min | {len(q)} questões")
    
    try:
        idx_quiz = ler_inteiro("Escolha o Quiz: ")
        quiz = quizzes[idx_quiz]
    except IndexError:
        print("Quiz inválido.")
        pausar()
        return

    if not usuario.pode_realizar_quiz(quiz):
        print(f"\nBLOQUEADO: Você já atingiu o limite de {quiz.tentativasLimite} tentativas.")
        pausar()
        return

    print(f"\nIniciando '{quiz.titulo}'... Boa sorte!")
    input(">>> Pressione ENTER para começar a prova <<<")
    
    try:
        tentativa = Tentativa(usuario, quiz)
    except ValueError as e:
        print(f"Erro: {e}")
        pausar()
        return
    
    for i, pergunta in enumerate(quiz.perguntas):
        limpar_tela()
        print(f"QUESTÃO {i+1}/{len(quiz)}: {pergunta.enunciado}")
        print(f"[{pergunta.dificuldade} | {pergunta.tema}]")
        print("-" * 40)
        
        for idx_alt, alt in enumerate(pergunta.alternativas):
            print(f"[{idx_alt}] {alt}")
        
        while True:
            r_int = ler_inteiro("\nSua resposta: ")
            if 0 <= r_int < len(pergunta.alternativas):
                tentativa.registrar_resposta(i, r_int)
                break
            print("Opção inválida.")

    print("\nFinalizando e calculando nota...")
    time.sleep(1)
    tentativa.finalizar()
    
    print("-" * 30)
    print(f"Nota Final: {tentativa.pontuacao:.2f}")
    print("Situação: " + ("APROVADO" if tentativa.aprovado else "REPROVADO"))
    
    limite_seg = quiz.tempoLimite * 60
    if tentativa.tempoGasto > limite_seg:
         print(f"TEMPO EXCEDIDO! A nota foi zerada.")
    
    pausar()

def fluxo_admin(usuarios: list[Usuario], quizzes: list[Quiz]):
    while True:
        op = menu_admin()
        
        if op == "1":
            rel = Relatorio(usuarios)
            if hasattr(rel, 'gerar_relatorio_alunos'):
                rel.gerar_relatorio_alunos()
            else:
                getattr(rel, 'exibir_relatorio', lambda: print("Erro no relatório"))()
            pausar()
        
        elif op == "2":
            criar_usuario_interativo(usuarios)
        
        elif op == "3":
            criar_quiz_interativo(quizzes)
            
        elif op == "4":
            adicionar_pergunta_a_quiz_existente(quizzes)
            
        elif op == "5":
            seed_data(usuarios, quizzes)
            pausar()
            
        elif op == "0":
            break
        else:
            print("Opção inválida.")
            pausar()

def seed_data(usuarios, quizzes):
    if quizzes:
        print("Já existem dados carregados.")
        return

    p1 = Pergunta("Quanto é 2+2?", ["3", "4", "5"], 1, "FÁCIL", "Matemática")
    p2 = Pergunta("Capital da França?", ["Rio", "Paris", "Londres"], 1, "FÁCIL", "Geo")
    q = Quiz("Demo Quiz", [p1, p2], tentativasLimite=3, tempoLimite=5)
    quizzes.append(q)
    
    u = Usuario("Aluno Teste", "aluno@teste.com", "202401")
    usuarios.append(u)
    print("Dados de exemplo criados!")

def users_check(lista):
    if not lista: 
        print("Nenhum usuário cadastrado.")
        return False
    return True

def quizzes_check(lista):
    if not lista: 
        print("Nenhum quiz disponível.")
        return False
    return True

def main():
    usuarios, quizzes = carregar_dados()
    
    while True:
        op = menu_principal()
        
        if op == "1":
            fluxo_responder_quiz(usuarios, quizzes)
        elif op == "2":
            fluxo_admin(usuarios, quizzes)
        elif op == "0":
            print("Salvando dados...")
            salvar_dados(usuarios, quizzes)
            print("Até logo!")
            break
        else:
            print("Opção inválida.")
            time.sleep(1)

if __name__ == "__main__":
    main()
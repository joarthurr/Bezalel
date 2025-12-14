import os
import time
import sys
from data.dados import carregar_dados, salvar_dados
from modules.Relatorio import Relatorio
from modules.Tentativa import Tentativa
from modules.Usuario import Usuario
from modules.Quiz import Quiz
from modules.Pergunta import Pergunta
from config.config import Config

try:
    import msvcrt
except ImportError:
    msvcrt = None

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPressione ENTER para continuar...")

def ler_inteiro(mensagem: str):
    """Funcao padrao para menus que nao precisam de timer."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada invalida. Digite um numero inteiro.")

def ler_input_com_tempo(mensagem: str, tentativa: Tentativa) -> str | None:
    """
    Le a entrada do usuario caractere por caractere, verificando o tempo
    a todo momento. Retorna a string digitada ou None se o tempo acabar.
    """
    print(mensagem, end='', flush=True)
    
    if msvcrt is None:
        print("[AVISO: Modo Timer indisponivel - usando input padrao]")
        return input()

    entrada = []
    
    while True:
        if tentativa.verificar_tempo_excedido():
            print("\n\n!!! TEMPO ESGOTADO !!!")
            return None

        if msvcrt.kbhit():
            char_bytes = msvcrt.getwch()
            
            if isinstance(char_bytes, bytes):
                char = char_bytes.decode('utf-8', 'ignore')
            else:
                char = char_bytes

            if char in ('\r', '\n'):
                print()
                return "".join(entrada)
            
            elif char == '\b':
                if entrada:
                    entrada.pop()
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            
            elif char.isprintable():
                entrada.append(char)
                sys.stdout.write(char)
                sys.stdout.flush()
        
        time.sleep(0.05)

def ler_inteiro_com_tempo(mensagem: str, tentativa: Tentativa) -> int:
    """Wrapper para converter o input temporal em inteiro."""
    while True:
        if tentativa.verificar_tempo_excedido():
            return -1 
            
        resultado = ler_input_com_tempo(mensagem, tentativa)
        
        if resultado is None:
            return -1
            
        try:
            return int(resultado)
        except ValueError:
            print("Entrada invalida. Digite um numero.")


def menu_principal():
    limpar_tela()
    print("="*40)
    print("      BEZALEL QUIZ SYSTEM v1.0")
    print("="*40)
    print("1. Area do Usuario (Responder)")
    print("2. Area Administrativa")
    print("0. Sair e Salvar")
    return input("\nEscolha uma opcao: ")

def menu_admin():
    limpar_tela()
    print("--- MENU ADMINISTRATIVO ---")
    print("1. Relatorio de Usuarios (Listagem)")
    print("2. Ranking de Desempenho")
    print("3. Estatisticas por Tema")
    print("4. Taxa de Acerto Global")
    print("5. Distribuicao de Notas")
    print("6. Cadastrar Novo Usuario")
    print("7. Criar Novo Quiz")
    print("8. Adicionar Pergunta a Quiz Existente")
    print("9. Gerar Dados de Teste (Seed)")
    print("0. Voltar")
    return input("\nEscolha uma opcao: ")

def criar_usuario_interativo(usuarios: list[Usuario]):
    print("\n--- Cadastro de Usuario ---")
    nome = input("Nome completo: ").strip()
    email = input("E-mail: ").strip()
    matricula = input("Matricula: ").strip()
    
    if not nome or not email or not matricula:
        print("Erro: Todos os campos sao obrigatorios.")
        pausar()
        return

    if any(u.matricula == matricula for u in usuarios):
        print(f"Erro: Ja existe um usuario com a matricula {matricula}.")
        pausar()
        return

    novo_user = Usuario(nome, email, matricula)
    usuarios.append(novo_user)
    print(f"Usuario {nome} cadastrado com sucesso!")
    pausar()

def criar_pergunta_interativa() -> Pergunta:
    print("\n--- Nova Pergunta ---")
    enunciado = input("Enunciado da questao: ").strip()
    tema = input("Tema (ex: Matematica, Historia): ").strip()
    
    print("Dificuldade (FACIL, MEDIO, DIFICIL):")
    dificuldade = input(">> ").strip().upper()

    mapa = {
        "FACIL": "fácil", "FÁCIL": "fácil",
        "MEDIO": "médio", "MÉDIO": "médio",
        "DIFICIL": "difícil", "DIFÍCIL": "difícil"
    }
    dificuldade = mapa.get(dificuldade, dificuldade.lower())
    
    print("\nCadastre as alternativas (Minimo 3, Maximo 5).")
    print("Deixe vazio e tecle ENTER para parar de adicionar.")
    alternativas = []
    while len(alternativas) < 5:
        alt = input(f"Alternativa {len(alternativas)}: ").strip()
        if not alt:
            if len(alternativas) >= 3:
                break
            else:
                print("Erro: Minimo de 3 alternativas necessarias.")
                continue
        alternativas.append(alt)
    
    print("\nQual e a alternativa correta?")
    for i, alt in enumerate(alternativas):
        print(f"[{i}] {alt}")
    
    while True:
        idx = ler_inteiro("Indice da correta: ")
        if 0 <= idx < len(alternativas):
            break
        print("Erro: Indice invalido.")

    return Pergunta(enunciado, alternativas, idx, dificuldade, tema)

def criar_quiz_interativo(quizzes: list[Quiz]):
    config = Config()
    
    print("\n--- Criacao de Quiz ---")
    titulo = input("Titulo do Quiz: ").strip()
    
    print(f"Limite de tentativas (Padrao: {config.tentativas_padrao}):")
    entrada_tent = input(">> ").strip()
    tentativas = int(entrada_tent) if entrada_tent else config.tentativas_padrao
    
    print(f"Tempo limite em minutos (Padrao: {config.tempo_padrao}):")
    entrada_tempo = input(">> ").strip()
    tempo = int(entrada_tempo) if entrada_tempo else config.tempo_padrao
    
    try:
        novo_quiz = Quiz(titulo, [], tentativas, tempo)
    except ValueError as e:
        print(f"Erro ao criar quiz: {e}")
        pausar()
        return

    print("\nAgora vamos adicionar perguntas.")
    while True:
        add = input("Deseja adicionar uma pergunta agora? (S/N): ").upper()
        if add != 'S': break
        try:
            pergunta = criar_pergunta_interativa()
            novo_quiz.adicionar_pergunta(pergunta)
            print("Pergunta adicionada!")
        except Exception as e:
            print(f"Erro: {e}")

    quizzes.append(novo_quiz)
    pausar()

def adicionar_pergunta_a_quiz_existente(quizzes: list[Quiz]):
    if not quizzes_check(quizzes): return
    
    print("\n--- Editar Quiz Existente ---")
    for i, q in enumerate(quizzes):
        print(f"{i}. {q.titulo} ({len(q)} questoes)")
    
    try:
        idx = ler_inteiro("Escolha o Quiz para editar: ")
        quiz = quizzes[idx]
    except IndexError:
        print("Erro: Quiz invalido.")
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

    print("--- Area do Usuario ---")
    print("Quem e voce?")
    for i, u in enumerate(usuarios):
        print(f"{i}. {u.nome} ({u.matricula})")
    
    try:
        idx_user = ler_inteiro("Seu numero: ")
        usuario = usuarios[idx_user]
    except IndexError:
        print("Erro: Usuario invalido.")
        pausar()
        return

    print(f"\nBem-vindo(a), {usuario.nome}!")
    print("Quizzes disponiveis:")
    for i, q in enumerate(quizzes):
        print(f"{i}. {q.titulo} | {q.tempoLimite} min | {len(q)} questoes")
    
    try:
        idx_quiz = ler_inteiro("Escolha o Quiz: ")
        quiz = quizzes[idx_quiz]
    except IndexError:
        print("Erro: Quiz invalido.")
        pausar()
        return

    if not usuario.pode_realizar_quiz(quiz):
        print(f"\nBLOQUEADO: Voce ja atingiu o limite de {quiz.tentativasLimite} tentativas.")
        pausar()
        return

    print(f"\nIniciando '{quiz.titulo}'... Voce tem {quiz.tempoLimite} minutos.")
    input(">>> Pressione ENTER para comecar a prova <<<")
    
    try:
        tentativa = Tentativa(usuario, quiz)
    except ValueError as e:
        print(f"Erro: {e}")
        pausar()
        return
    
    if msvcrt:
        print("[DEBUG: Sistema de Timer Ativo]")
    
    tempo_esgotado = False
    
    for i, pergunta in enumerate(quiz.perguntas):
        if tentativa.verificar_tempo_excedido():
            tempo_esgotado = True
            break
            
        limpar_tela()
        print(f"QUESTAO {i+1}/{len(quiz)}: {pergunta.enunciado}")
        print(f"[{pergunta.dificuldade} | {pergunta.tema}]")
        print("-" * 40)
        
        for idx_alt, alt in enumerate(pergunta.alternativas):
            print(f"[{idx_alt}] {alt}")
        
        while True:
            r_int = ler_inteiro_com_tempo("\nSua resposta: ", tentativa)
            
            if r_int == -1 and tentativa.verificar_tempo_excedido():
                tempo_esgotado = True
                break
            
            if 0 <= r_int < len(pergunta.alternativas):
                tentativa.registrar_resposta(i, r_int)
                break
            
            if not tempo_esgotado:
                print("Opcao invalida.")
        
        if tempo_esgotado:
            break

    print("\nFinalizando...")
    tentativa.finalizar()
    
    print("-" * 30)
    
    if tempo_esgotado or tentativa.tempoGasto > quiz.tempoLimite*60:
         print(f"TEMPO ACABADO! O quiz foi encerrado e a nota zerada.")
    
    print(f"Nota Final: {tentativa.pontuacao:.2f}")
    print("Situacao: " + ("APROVADO" if tentativa.aprovado else "REPROVADO"))
    
    pausar()

def fluxo_admin(usuarios: list[Usuario], quizzes: list[Quiz]):
    while True:
        op = menu_admin()
        rel = Relatorio(usuarios)
        
        if op == "1":
            rel.gerar_relatorio_usuarios()
            pausar()
        elif op == "2":
            rel.gerar_ranking()
            pausar()
        elif op == "3":
            rel.gerar_desempenho_por_tema()
            pausar()
        elif op == "4":
            rel.gerar_taxa_acerto_global()
            pausar()
        elif op == "5":
            rel.gerar_distribuicao_notas()
            pausar()
        elif op == "6":
            criar_usuario_interativo(usuarios)
        elif op == "7":
            criar_quiz_interativo(quizzes)
        elif op == "8":
            adicionar_pergunta_a_quiz_existente(quizzes)
        elif op == "9":
            seed_data(usuarios, quizzes)
            pausar()
        elif op == "0":
            break
        else:
            print("Opcao invalida.")
            pausar()

def seed_data(usuarios, quizzes):
    if quizzes:
        print("Aviso: Ja existem dados carregados.")
        return

    p1 = Pergunta("Quanto e 2+2?", ["3", "4", "5"], 1, "FACIL", "Matematica")
    p2 = Pergunta("Capital da Franca?", ["Rio", "Paris", "Londres"], 1, "FACIL", "Geo")
    p3 = Pergunta("Raiz de 144?", ["10", "11", "12"], 2, "MEDIO", "Matematica")
    q = Quiz("Demo Quiz", [p1, p2, p3], tentativasLimite=3, tempoLimite=5)
    quizzes.append(q)
    
    u = Usuario("Usuario Teste", "usuario@teste.com", "202401")
    usuarios.append(u)
    print("Dados de exemplo criados!")

def users_check(lista):
    if not lista: 
        print("Aviso: Nenhum usuario cadastrado.")
        return False
    return True

def quizzes_check(lista):
    if not lista: 
        print("Aviso: Nenhum quiz disponivel.")
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
            print("Ate logo!")
            break
        else:
            print("Opcao invalida.")
            time.sleep(1)

if __name__ == "__main__":
    main()
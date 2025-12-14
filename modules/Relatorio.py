from modules.Usuario import Usuario

class Relatorio:
    def __init__(self, usuarios: list[Usuario]):
        self.usuarios = usuarios

    def gerar_relatorio_usuarios(self):
        """Relatorio Basico: Listagem de usuarios e quantidade de provas."""
        print("\n" + "="*60)
        print(f"{'RELATORIO GERAL DE USUARIOS':^60}")
        print("="*60)
        
        if not self.usuarios:
            print("Nenhum usuario cadastrado.")
            return

        print(f"{'Matricula':<12} | {'Nome':<25} | {'Tentativas'}")
        print("-" * 60)
        for user in self.usuarios:
            qtd = len(user.obter_relatorio())
            print(f"{user.matricula:<12} | {user.nome:<25} | {qtd:^10}")
        print("-" * 60)

    def gerar_ranking(self):
        """
        Relatorio Avancado: Ranking de usuarios por media de notas.
        Ignora tentativas incompletas ou encerradas por tempo.
        """
        print("\n" + "="*60)
        print(f"{'RANKING DE DESEMPENHO (Media Global)':^60}")
        print("="*60)

        dados_ranking = []

        for user in self.usuarios:
            tentativas_totais = user.obter_relatorio()
            
            tentativas = [
                t for t in tentativas_totais 
                if t.concluida and not getattr(t, 'incompleta', False)
            ]

            if not tentativas:
                continue
            
            soma_notas = sum(t.pontuacao for t in tentativas)
            media = soma_notas / len(tentativas)
            dados_ranking.append({
                "nome": user.nome,
                "media": media,
                "provas": len(tentativas)
            })

        dados_ranking.sort(key=lambda x: x["media"], reverse=True)

        if not dados_ranking:
            print("Nenhum dado de desempenho valido disponivel.")
            return

        print(f"{'Pos':<4} | {'Nome':<25} | {'Media':<10} | {'Provas'}")
        print("-" * 60)
        
        for i, dado in enumerate(dados_ranking):
            print(f"{i+1:<4} | {dado['nome']:<25} | {dado['media']:<10.2f} | {dado['provas']}")
        print("-" * 60)

    def gerar_desempenho_por_tema(self):
        """Relatorio Consolidado: Desempenho por Tema."""
        print("\n" + "="*60)
        print(f"{'ESTATISTICAS POR TEMA (Global)':^60}")
        print("="*60)

        estatisticas = {}
        tem_dados = False

        for user in self.usuarios:
            for tentativa in user.obter_relatorio():
                if not tentativa.concluida or getattr(tentativa, 'incompleta', False):
                    continue
                
                tem_dados = True
                quiz = tentativa.quiz
                respostas = tentativa.respostasDadas

                for i, pergunta in enumerate(quiz.perguntas):
                    tema = pergunta.tema.strip().upper()
                    
                    if tema not in estatisticas:
                        estatisticas[tema] = {'acertos': 0, 'total': 0}
                    
                    estatisticas[tema]['total'] += 1
                    
                    if i < len(respostas) and respostas[i] == pergunta.indiceCorreta:
                        estatisticas[tema]['acertos'] += 1

        if not tem_dados:
            print("Nenhuma tentativa valida para gerar estatisticas.")
            return

        print(f"{'Tema':<20} | {'Total Quest.':<12} | {'Acertos':<10} | {'% Sucesso'}")
        print("-" * 60)
        
        for tema, dados in estatisticas.items():
            total = dados['total']
            acertos = dados['acertos']
            taxa = (acertos / total * 100) if total > 0 else 0.0
            print(f"{tema:<20} | {total:<12} | {acertos:<10} | {taxa:.1f}%")
        print("-" * 60)

    def gerar_taxa_acerto_global(self):
        """Relatorio de Taxa de Acerto Global."""
        print("\n" + "="*60)
        print(f"{'TAXA DE ACERTO DO SISTEMA':^60}")
        print("="*60)

        total_questoes_respondidas = 0
        total_acertos = 0

        for user in self.usuarios:
            for tentativa in user.obter_relatorio():
                if not tentativa.concluida or getattr(tentativa, 'incompleta', False):
                    continue
                
                quiz = tentativa.quiz
                for i, resp in enumerate(tentativa.respostasDadas):
                    if i < len(quiz.perguntas):
                        total_questoes_respondidas += 1
                        if resp == quiz.perguntas[i].indiceCorreta:
                            total_acertos += 1
        
        if total_questoes_respondidas == 0:
            print("Sem dados suficientes.")
            return

        taxa = (total_acertos / total_questoes_respondidas) * 100
        print(f"Total de questoes respondidas: {total_questoes_respondidas}")
        print(f"Total de acertos: {total_acertos}")
        print(f"Taxa Global de Sucesso: {taxa:.2f}%")
        print("-" * 60)

    def gerar_distribuicao_notas(self):
        """Relatorio de Distribuicao de Notas (Histograma)."""
        print("\n" + "="*60)
        print(f"{'DISTRIBUICAO DE NOTAS':^60}")
        print("="*60)

        faixas = {
            "0-49": 0,
            "50-69": 0,
            "70-89": 0,
            "90-100": 0
        }

        for user in self.usuarios:
            for t in user.obter_relatorio():
                if not t.concluida or getattr(t, 'incompleta', False):
                    continue

                nota = t.pontuacao

                if nota < 50:
                    faixas["0-49"] += 1
                elif nota < 70:
                    faixas["50-69"] += 1
                elif nota < 90:
                    faixas["70-89"] += 1
                else:
                    faixas["90-100"] += 1

        total = sum(faixas.values())

        if total == 0:
            print("Nenhuma tentativa valida para analise.")
            return

        print(f"{'Faixa':<10} | {'Qtd':<5} | {'%'}")
        print("-" * 30)
        for faixa, qtd in faixas.items():
            perc = (qtd / total) * 100
            print(f"{faixa:<10} | {qtd:<5} | {perc:.2f}%")
        print("-" * 30)
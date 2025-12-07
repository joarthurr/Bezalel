from modules.Usuario import Usuario

class Relatorio:
    def __init__(self, usuarios: list[Usuario]):
        self.usuarios = usuarios

    def gerar_relatorio_usuarios(self):
        """Relatorio Basico: Listagem de usuarios e quantidade de provas."""
        print("\n" + "="*50)
        print(f"{'RELATORIO DE USUARIOS':^50}")
        print("="*50)
        
        if not self.usuarios:
            print("Nenhum usuario cadastrado.")
            return

        print(f"{'Matricula':<12} | {'Nome':<25} | {'Tentativas'}")
        print("-" * 55)
        for user in self.usuarios:
            qtd = len(user.obter_relatorio())
            print(f"{user.matricula:<12} | {user.nome:<25} | {qtd:^10}")
        print("-" * 55)

    def gerar_ranking(self):
        """
        Relatorio Avancado: Ranking de usuarios por media de notas.
        Calcula a media de todas as tentativas de cada usuario.
        """
        print("\n" + "="*50)
        print(f"{'RANKING DE DESEMPENHO (Media Global)':^50}")
        print("="*50)

        dados_ranking = []

        for user in self.usuarios:
            tentativas = user.obter_relatorio()
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
            print("Nenhum dado de desempenho disponivel.")
            return

        print(f"{'Pos':<4} | {'Nome':<25} | {'Media':<10} | {'Provas'}")
        print("-" * 55)
        
        for i, dado in enumerate(dados_ranking):
            print(f"{i+1:<4} | {dado['nome']:<25} | {dado['media']:<10.2f} | {dado['provas']}")
        print("-" * 55)
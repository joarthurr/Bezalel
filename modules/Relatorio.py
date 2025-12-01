from modules.Usuario import Usuario

class Relatorio:
    def __init__(self, usuarios: list[Usuario]):
        self.usuarios = usuarios

    def exibir_relatorio(self):
        print("\n--- Relatório ---")
        if not self.usuarios:
            print("Nenhum usuário cadastrado.")
            return

        print(f"{'Matrícula':<15} | {'Nome':<30} | {'Tentativas'}")
        print("-" * 60)
        for user in self.usuarios:
            qtd = len(user.obter_relatorio())
            print(f"{user.matricula:<15} | {user.nome:<30} | {qtd}")
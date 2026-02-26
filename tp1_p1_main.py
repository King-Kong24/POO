import os
from tripulante import tripulante
from navio import navio

FUNCOES_DISPONIVEIS = [
    "Capitão",
    "Navegador",
    "Médico",
    "Cozinheiro",
    "Atirador de Elite",
    "Arqueologista",
    "Construtor Naval",
    "Músico",
    "Timoneiro"
]

def limpar_terminal():
    os.system('cls')

def mostrar_menu():
    print("\n1 - Criar Navio" \
        "\n2 - Recrutar Tripulante" \
        "\n3 - Expulsar Tripulante" \
        "\n4 - Mostrar Manifesto" \
        "\n5 - Sair")

def main():
    while True:
        mostrar_menu()
        op = input("Escolha: ").strip()
        if op == '1':
            limpar_terminal()
            nome_navio = input("Digite o nome do navio: ")
            limpar_terminal()
            navio1 = navio(nome_navio)
            print(f"Navio '{nome_navio}' criado com sucesso!")
            input("Pressione ENTER para continuar...")
            limpar_terminal()
        elif op == '2':
            if 'navio1' not in locals():
                print("Erro: Crie um navio primeiro.")
                input("Pressione ENTER para continuar...")
                limpar_terminal()
                continue
            limpar_terminal()
            nome = input("Digite o nome do tripulante: ")
            limpar_terminal()
            
            # Menu de seleção de função
            print("\nEscolha a função do tripulante:")
            for i, func in enumerate(FUNCOES_DISPONIVEIS, 1):
                print(f"{i} - {func}")
            opcao_funcao = input("Escolha a função (número): ").strip()
            
            try:
                indice = int(opcao_funcao) - 1
                if 0 <= indice < len(FUNCOES_DISPONIVEIS):
                    funcao = FUNCOES_DISPONIVEIS[indice]
                else:
                    print("Opção inválida! Tente novamente.")
                    input("Pressione ENTER para continuar...")
                    limpar_terminal()
                    continue
            except ValueError:
                print("Entrada inválida! Tente novamente.")
                input("Pressione ENTER para continuar...")
                limpar_terminal()
                continue
            
            limpar_terminal()
            recompensa = float(input("Digite a recompensa do tripulante: "))
            limpar_terminal()
            poder = int(input("Digite o poder do tripulante (0-100): "))
            limpar_terminal()
            energia = int(input("Digite a energia do tripulante (0-100): "))
            limpar_terminal()
            novo_tripulante = tripulante(nome, funcao, recompensa, poder, energia)
            navio1.recrutar(novo_tripulante)
            print(f"Tripulante '{nome}' recrutado com sucesso!")
            input("Pressione ENTER para continuar...")
            limpar_terminal()
        elif op == '3':
            if 'navio1' not in locals():
                print("Erro: Crie um navio primeiro.")
                input("Pressione ENTER para continuar...")
                limpar_terminal()
                continue
            limpar_terminal()
            nome_tripulante = input("Digite o nome do tripulante a expulsar: ")
            navio1.expulsar(nome_tripulante)
            print(f"Tripulante '{nome_tripulante}' expulso com sucesso!")
            input("Pressione ENTER para continuar...")
            limpar_terminal()
        elif op == '4':
            if 'navio1' not in locals():
                print("Erro: Crie um navio primeiro.")
                input("Pressione ENTER para continuar...")
                limpar_terminal()
                continue
            limpar_terminal()
            navio1.mostrar_manifesto()
            input("Pressione ENTER para continuar...")
            limpar_terminal()
        elif op == '5':
            limpar_terminal()
            print("Adeus!")
            break
if __name__ == "__main__":
    main()
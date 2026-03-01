import os
from tripulante import tripulante
from navio import navio
from persistencia import salvar_navio, carregar_navio

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

def main():
    meu_navio = None
    
    while True:
        print("\n--- One Piece: Grand Line Adventures ---")
        print("1 - Criar Navio")
        print("2 - Recrutar Tripulante")
        print("3 - Expulsar Tripulante")
        print("4 - Mostrar Manifesto")
        print("5 - Sair")
        print("6 - Salvar Navio")
        print("7 - Carregar Navio")

        op = input("Escolha: ").strip()

        if op == '1':
            limpar_terminal()
            nome = input("Nome do Navio: ")
            meu_navio = navio(nome)
            print(f"Navio {nome} pronto para navegar.")

        elif op == '2':
            limpar_terminal()
            if meu_navio is None:
                print("Crie um navio primeiro.")
                continue
            
            try:
                nome = input("Nome: ")
                func = input("Função: ")
                recompensa = float(input("Bounty (M): "))
                poder = int(input("Poder (0-100): "))
                energia = int(input("Energia (0-100): "))
                
                novo = tripulante(nome, func, recompensa, poder, energia)
                if meu_navio.recrutar(novo):
                    print("Recrutado.")
            except ValueError as e:
                print(f"Erro nos dados: {e}")

        elif op == '3':
            limpar_terminal()
            if meu_navio:
                nome = input("Nome do pirata a expulsar: ")
                if meu_navio.expulsar(nome):
                    print(f"{nome} foi deixado na ilha mais próxima.")
                else:
                    print("Tripulante não encontrado.")

        elif op == '4':
            limpar_terminal()
            if meu_navio:
                meu_navio.mostrar_manifesto()
            else:
                print("Sem navio, sem manifesto.")

        elif op == '5':
            limpar_terminal()
            print("Rumo a Laugh Tale." \
            "\nAté a próxima aventura.")
            break

        elif op == '6':
            if meu_navio:
                meu_navio.salvar()

        elif op == '7':
            carregado = carregar_navio()
            if carregado:
                meu_navio = carregado
                print("Navio carregado com sucesso")
            else:
                print("Nenhum navio foi carregado.")

if __name__ == "__main__":
    main()
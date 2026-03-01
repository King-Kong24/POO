"""One Piece: Grand Line Adventures - Parte 1 (Menu Principal)

Programa interativo para gerenciar uma tripulação pirata.
Permite recrutar tripulantes, definir habilidades, guardar e carregar o estado do navio.

Execute com: python tp1_p1_main.py
"""

import os
from colorama import Style
from tripulante import Tripulante
from navio import Navio
from persistencia import carregar_navio

# Lista de funções disponíveis para recrutar tripulantes (apenas Tripulante básico implementado)
funcoes_disponiveis = [
    "Capitão",
    "Espadachim",
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
    """Limpa a tela do terminal para melhor visualização.
    
    Usa o comando 'cls' no Windows.
    Para Linux/Mac, alterar para 'clear'.
    """
    os.system('cls')

def main():
    """Função principal que executa o menu interativo do jogo.
    
    Permite ao utilizador:
    - Criar um novo navio
    - Recrutar tripulantes
    - Expulsar tripulantes
    - Mostrar manifesto da tripulação
    - Colocar tripulantes a trabalhar/descansar
    - Salvar e carregar o estado do navio
    """
    meu_navio = None
    
    while True:
        limpar_terminal()
        print("\n--- One Piece: Grand Line Adventures ---")
        print("1 - Criar Navio")
        print("2 - Recrutar Tripulante")
        print("3 - Expulsar Tripulante")
        print("4 - Mostrar Manifesto")
        print("5 - Colocar Tripulante a Trabalhar")
        print("6 - Colocar Tripulante a Descansar")
        print("7 - Salvar Navio")
        print("8 - Carregar Navio")
        print("9 - Sair")
        print(Style.RESET_ALL)

        op = input("Escolha: ").strip()

        # Opção 1: Criar um novo navio
        if op == '1':
            limpar_terminal()
            nome = input("Nome do Navio: ")
            meu_navio = Navio(nome)
            print(f"Navio {nome} pronto para navegar.")

        # Opção 2: Recrutar um novo tripulante
        elif op == '2':
            limpar_terminal()
            if meu_navio is None:
                print("Crie um navio primeiro.")
                continue
            
            try:
                nome = input("Nome: ")
            
                print("\nEscolha a função do tripulante:")
                for i, func in enumerate(funcoes_disponiveis, 1):
                    print(f"{i} - {func}")
                opcao_funcao = input("Escolha a função (número): ").strip()
            
                try:
                    indice = int(opcao_funcao) - 1
                    if 0 <= indice < len(funcoes_disponiveis):
                        funcao = funcoes_disponiveis[indice]
                    else:
                        print("Opção inválida! Tente novamente.")
                        input("Pressione ENTER para continuar...")
                        limpar_terminal()
                    
                except ValueError:
                    print("Entrada inválida! Tente novamente.")
                    input("Pressione ENTER para continuar...")
                    limpar_terminal()
                
                # Solicita as características do tripulante
                recompensa = float(input("Bounty (M): "))
                poder = int(input("Poder (0-100): "))
                energia = int(input("Energia (0-100): "))
                
                # Cria e recruta o novo tripulante
                novo = Tripulante(nome, recompensa, poder, energia)
                if meu_navio.recrutar(novo):
                    print("Recrutado")
            except ValueError as e:
                print(f"Erro nos dados: {e}")

        # Opção 3: Expulsar um tripulante
        elif op == '3':
            limpar_terminal()
            if meu_navio:
                print("Quem que vai ser expulso?")
                for i, t in enumerate(meu_navio.tripulacao, 1):
                    print(f"{i} - {t.nome}")
                try:
                    escolha = int(input("Escolha o número do tripulante: ")) - 1
                    if 0 <= escolha < len(meu_navio.tripulacao):
                        nome = meu_navio.tripulacao[escolha].nome
                        if meu_navio.expulsar(nome):
                            print(f"{nome} foi deixado na ilha mais próxima.")
                            input("\nPressione ENTER para continuar...")
                            limpar_terminal()
                        else:
                            print("Tripulante não encontrado.")
                            input("\nPressione ENTER para continuar...")
                    else:
                        print("Escolha inválida.")
                        input("\nPressione ENTER para continuar...")
                except ValueError:
                    print("Entrada inválida. Digite um número.")
                    input("\nPressione ENTER para continuar...")

        # Opção 4: Mostrar o manifesto (lista de tripulantes)
        elif op == '4':
            limpar_terminal()
            if meu_navio:
                meu_navio.mostrar_manifesto()
                input("\nPressione ENTER para continuar...")
            else:
                print("Sem navio, sem manifesto.")
                input("Pressione ENTER para continuar")
                limpar_terminal()

        # Opção 5: Colocar um tripulante a trabalhar (reduz energia)
        elif op == '5':
            limpar_terminal()
            if meu_navio and meu_navio.tripulacao:
                print("--- Quem vai trabalhar? ---")
                for i, t in enumerate(meu_navio.tripulacao, 1):
                    print(f"{i} - {t.nome} (Energia: {t.energia})")
                
                try:
                    escolha = int(input("Escolha o número do tripulante: ")) - 1
                    if 0 <= escolha < len(meu_navio.tripulacao):
                        pirata = meu_navio.tripulacao[escolha]
                        horas = int(input(f"Quantas horas de trabalho para {pirata.nome}? "))
                        pirata.trabalhar(horas)
                        print(f"\n{pirata.nome} trabalhou arduamente.")
                    else:
                        print("Escolha inválida.")
                except ValueError:
                    print("Entrada inválida. Digite um número.")
                input("\nPressione ENTER para continuar...")
                limpar_terminal()
            else:
                print("Não há tripulação disponível.")
                input("Pressione ENTER para continuar...")
                limpar_terminal()

        # Opção 6: Colocar um tripulante a descansar (recupera energia)
        elif op == '6':
            limpar_terminal()
            if meu_navio and meu_navio.tripulacao:
                print("--- Quem vai descansar? ---")
                for i, t in enumerate(meu_navio.tripulacao, 1):
                    print(f"{i} - {t.nome} (Energia: {t.energia})")
                
                try:
                    escolha = int(input("Escolha o número do tripulante: ")) - 1
                    if 0 <= escolha < len(meu_navio.tripulacao):
                        pirata = meu_navio.tripulacao[escolha]
                        pirata.descansar()
                        print(f"\n{pirata.nome} está como novo")
                    else:
                        print("Escolha inválida.")
                except ValueError:
                    print("Entrada inválida. Digite um número.")
                
                input("\nPressione ENTER para continuar...")
                limpar_terminal()
            else:
                print("Não há tripulação disponível.")
                input("Pressione ENTER para continuar...")
                limpar_terminal()

        # Opção 7: Salvar o estado do navio
        elif op == '7':
            limpar_terminal()
            if meu_navio:
                meu_navio.salvar()
                print("Navio salvo com sucesso.")
                input("Pressione ENTER para continuar")
                limpar_terminal()
           
        # Opção 8: Carregar um navio guardado
        elif op == '8':
            limpar_terminal()
            carregado = carregar_navio()
            if carregado:
                meu_navio = carregado
                print("Navio carregado com sucesso")
                input("Pressione ENTER para continuar")
            else:
                print("Nenhum navio foi carregado.")
                input("Pressione ENTER para continuar")
                limpar_terminal()

        # Opção 9: Sair do programa
        elif op == '9':
            limpar_terminal()
            print("Rumo a Laugh Tale." \
            "\nAté a próxima aventura.")
            break


if __name__ == "__main__":
    main()
#uv run tp1_p2_main.py
# /// script
# requires-python = ">=3.10"
# ///
"""
One Piece — Grand Line Adventures (Parte 2)
===========================================
Programa principal do TP1.

Este ficheiro contém a simulação atualizada com mecânicas de:
- Vida do Navio (Game Over se chegar a 0)
- Ouro (Pontuação extra)
- Status da Tripulação

Execute com: uv run tp1_p2_main.py
"""

import os
import random
import sys
import time
from colorama import Fore, Style, init

from navio import Navio
from tripulante import Tripulante
from espadachim import Espadachim
from navegador import Navegador
from medico import Medico
from cozinheiro import Cozinheiro
from persistencia import salvar_navio, carregar_navio

init(autoreset=True)


class Evento:
    """Representa um evento aleatório que ocorre durante a aventura."""

    def __init__(self, nome, descricao, dano_vida=0, dano_energia=0, recompensa=0, tipo_ideal=None):
        """Inicializa um evento.

        Args:
            nome: Nome do evento.
            descricao: Descrição narrativa.
            dano_vida: Dano ao navio se falhar.
            dano_energia: Dano à tripulação se falhar.
            recompensa: Ouro ganho se tiver sucesso.
            tipo_ideal: Classe ideal para resolver o evento.
        """
        self.nome = nome
        self.descricao = descricao
        self.dano_vida = dano_vida
        self.dano_energia = dano_energia
        self.recompensa = recompensa
        self.tipo_ideal = tipo_ideal


class Simulacao:
    """Motor principal do jogo Grand Line Adventures."""

    EVENTOS = [
        Evento("🦑 Kraken",
               "Um monstro gigante surge do abismo!",
               dano_vida=30, dano_energia=10, recompensa=500,
               tipo_ideal="Espadachim"),
        Evento("🌪️  Tempestade Ciclópica",
               "Ondas de 20 metros ameaçam virar o navio!",
               dano_vida=40, dano_energia=5, recompensa=100,
               tipo_ideal="Navegador"),
        Evento("⚓ Marinha - Bloqueio",
               "Navios de guerra bloqueiam a passagem!",
               dano_vida=20, dano_energia=20, recompensa=300,
               tipo_ideal="Espadachim"),
        Evento("🍒 Escorbuto",
               "A falta de vitamina C está a afetar a tripulação...",
               dano_vida=0, dano_energia=30, recompensa=0,
               tipo_ideal="Cozinheiro"), # Cozinheiro previne com boa comida
        Evento("🦠 Vírus Desconhecido",
               "Vários tripulantes estão com febre alta.",
               dano_vida=0, dano_energia=40, recompensa=0,
               tipo_ideal="Medico"),
        Evento("🗺️  Mapa do Tesouro",
               "Encontraram uma garrafa com um mapa antigo!",
               dano_vida=0, dano_energia=0, recompensa=1000,
               tipo_ideal="Navegador"),
        Evento("🧜 Sereias",
               "O canto das sereias está a atrair o navio para as rochas!",
               dano_vida=25, dano_energia=10, recompensa=200,
               tipo_ideal="Medico"), # Médico/Músico resiste mentalmente? Vamos assumir Médico por agora.
    ]

    MAX_TURNOS = 10

    def __init__(self, navio):
        self.navio = navio
        self.turno_atual = 0

    def _imprimir_lento(self, texto, delay=0.01):
        """Imprime texto com um pequeno delay para efeito dramático (opcional)."""
        print(texto)
        # sys.stdout.flush()
        # time.sleep(delay) # Descomentar para efeito "typewriter"

    def _cabecalho(self):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"  TURNO {self.turno_atual}/{self.MAX_TURNOS}")
        print(f"{'='*60}{Style.RESET_ALL}\n")

    def _menu_trabalhar(self):
        print("\n  --- Quem vai trabalhar? ---")
        for i, t in enumerate(self.navio.tripulacao, 1):
            print(f"  {i} - {t.nome} (Energia: {t.energia})")
        try:
            escolha = int(input("  Escolha o número do tripulante: ")) - 1
            if 0 <= escolha < len(self.navio.tripulacao):
                pirata = self.navio.tripulacao[escolha]
                horas = int(input(f"  Quantas horas de trabalho para {pirata.nome}? "))
                pirata.trabalhar(horas)
                print(f"  {Fore.YELLOW}{pirata.nome} trabalhou arduamente.{Style.RESET_ALL}")
            else:
                print("  ❌ Escolha inválida.")
        except ValueError:
            print("  ❌ Entrada inválida.")
        input("\n  [Enter] para voltar...")

    def _menu_descansar(self):
        print("\n  --- Quem vai descansar? ---")
        for i, t in enumerate(self.navio.tripulacao, 1):
            print(f"  {i} - {t.nome} (Energia: {t.energia})")
        try:
            escolha = int(input("  Escolha o número do tripulante: ")) - 1
            if 0 <= escolha < len(self.navio.tripulacao):
                pirata = self.navio.tripulacao[escolha]
                pirata.descansar()
                print(f"  {Fore.GREEN}{pirata.nome} está como novo!{Style.RESET_ALL}")
            else:
                print("  ❌ Escolha inválida.")
        except ValueError:
            print("  ❌ Entrada inválida.")
        input("\n  [Enter] para voltar...")

    def _escolher_tripulante(self):
        tripulacao = [t for t in self.navio.tripulacao if t.energia > 0]
        
        if not tripulacao:
            return None

        print("  Quem vai lidar com isto?")
        for i, t in enumerate(tripulacao, 1):
            print(f"  {i}. {t.nome} ({type(t).__name__}) - E:{t.energia}")
        
        while True:
            try:
                opcao = int(input("\n  Escolha o número: "))
                if 1 <= opcao <= len(tripulacao):
                    return tripulacao[opcao - 1]
            except ValueError:
                pass
            print("  ❌ Opção inválida.")

    def _resolver_evento(self, evento, tripulante):
        print(f"\n  ➡️  {tripulante.nome} avança para resolver o problema!")
        
        # Polimorfismo: O tripulante executa a sua ação
        # Nota: Na Parte 2, executar_acao recebe o navio.
        # A lógica específica de "combate" vs "navegação" é abstrata no método,
        # mas aqui validamos se a CLASSE do tripulante é a correta para o evento.
        tripulante.executar_acao(self.navio)
        tripulante.trabalhar(10) # Custa sempre energia agir

        sucesso = (type(tripulante).__name__ == evento.tipo_ideal)

        if sucesso:
            self._imprimir_lento(f"  ✅{Fore.GREEN} SUCESSO! {Style.RESET_ALL}{tripulante.nome} sabia exatamente o que fazer.")
            ganho = evento.recompensa
            if ganho > 0:
                print(f"  💰 {Fore.YELLOW}Tesouro obtido: {ganho} berry!{Style.RESET_ALL}")
                self.navio.ganhar_ouro(ganho)
            else:
                print("  O navio está seguro... por agora.")
        else:
            self._imprimir_lento(f"  ❌ {Fore.RED}FALHA! {Style.RESET_ALL}{tripulante.nome} tentou, mas não era a pessoa certa...")


            if getattr(self.navio, "rota_segura", False):
                print(f"{Fore.CYAN}Graças à rota segura traçada pelo Navegador, o dano ao navio foi mitigado!")
                self.navio.rota_segura = False
            else:
                print(f"  💥 O navio sofre {evento.dano_vida} de dano!")
                self.navio.danificar(evento.dano_vida)
            if evento.dano_energia > 0:
                print(f"  😓 A tripulação perde {evento.dano_energia} de energia.")
                for t in self.navio.tripulacao:
                    t.trabalhar(evento.dano_energia / 5) # Conversão aproximada
        mortos = [t for t in self.navio.tripulacao if t.energia <= 0]
        if mortos:
            print(f"\n  {Fore.RED}⚠️  Tripulantes que não resistiram:{Style.RESET_ALL}")
            for defunto in mortos:
                print(f"  O corpo de {defunto.nome} foi lançado ao mar...")
                self.navio.expulsar(defunto.nome)


    def jogar(self):
        print(f"\n\n{Fore.YELLOW}{'='*60}")
        print("ONE PIECE: GRAND LINE ADVENTURES (PARTE 2)")
        print("Sobrevivam à Grand Line e acumulem o maior tesouro!")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")

        for i in range(1, self.MAX_TURNOS + 1):
            self.turno_atual = i
            evento = random.choice(self.EVENTOS)

            while True:
                limpar_terminal()
                self._cabecalho()
                self.navio.mostrar_manifesto()

                if self.navio.vida <= 0:
                    print(f"\n  💀 {Fore.RED}O navio foi destruído! Game Over.{Style.RESET_ALL}")
                    return

                print(f"\n  🎲 {Fore.MAGENTA}EVENTO DO TURNO: {evento.nome}{Style.RESET_ALL}")
                print(f"     \"{evento.descricao}\"")
                print(f"     (Ideal: {evento.tipo_ideal})\n")

                print("  O que deseja fazer?")
                print("  1 -  Enfrentar o Evento")
                print("  2 - Colocar Tripulante a Descansar")
                print("  3 -  Colocar Tripulante a Trabalhar")

                opcao = input("\n  Escolha: ").strip()

                if opcao == '1':
                    break
                elif opcao == '2':
                    self._menu_descansar()
                elif opcao == '3':
                    self._menu_trabalhar()
                else:
                    print("  ❌ Opção inválida.")

            tripulante = self._escolher_tripulante()
            if not tripulante:
                print(f"  💤 {Fore.CYAN}Toda a tripulação está exausta! O navio fica à deriva...{Style.RESET_ALL}")
                self.navio.danificar(evento.dano_vida)
                if i < self.MAX_TURNOS:
                    input("\n  [Enter] para continuar...")
                continue

            self._resolver_evento(evento, tripulante)
            
            # Pausa para leitura
            if i < self.MAX_TURNOS:
                input("\n  [Enter] para continuar...")

        self._fim_de_jogo()

    def _fim_de_jogo(self):
        print("\n\n" + "="*60)
        print("  RELATÓRIO FINAL")
        print("="*60)
        self.navio.mostrar_manifesto()
        
        if self.navio.vida > 0:
            print(f"\n  🎉 {Fore.GREEN}PARABÉNS! Chegaram ao fim da rota.{Style.RESET_ALL}")
            score = self.navio.ouro + (self.navio.vida * 10)
            print(f"  🏆 {Fore.YELLOW}Pontuação Final: {score}{Style.RESET_ALL}")
        else:
            print(f"\n  💀 {Fore.RED}A vossa aventura acabou no fundo do mar!{Style.RESET_ALL}")


def criar_tripulacao_predefinida():
    navio = Navio("Going Merry 2.0")
    
    navio.recrutar(Espadachim("Zoro", recompensa=320.0, poder=90, espadas=["Wado", "Enma"]))
    navio.recrutar(Navegador("Nami", recompensa=66.0, poder=40, milhas_navegadas=1000))
    navio.recrutar(Medico("Chopper", recompensa=0.1, poder=30, pacientes_curados=50))
    navio.recrutar(Cozinheiro("Sanji", recompensa=330.0, poder=85, refeicoes_preparadas=500))
    return navio

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    meu_navio = None

    while True:
        limpar_terminal()
        print(f"\n{Fore.YELLOW}--- One Piece: Grand Line Adventures (Parte 2) ---{Style.RESET_ALL}")
        if meu_navio:
            print(f"Navio atual: {Fore.GREEN}{meu_navio.nome}{Style.RESET_ALL} ({Fore.RED}Vida: {meu_navio.vida} {Style.RESET_ALL}| Tripulantes: {len(meu_navio.tripulacao)})")
        else:
            print(f"Navio atual: {Fore.RED}Nenhum{Style.RESET_ALL}")
                
        print("\n0 - Iniciar Simulação (Zarpar para a Grand Line!)")
        print("1 - Criar Navio Personalizado")
        print("2 - Recrutar Tripulante")
        print("3 - Expulsar Tripulante")
        print("4 - Mostrar Manifesto")
        print("5 - Salvar Navio")
        print("6 - Carregar Navio")
        print("7 - Carregar Tripulação Predefinida")
        print("8 - Sair")

        op = input("\nEscolha: ").strip()

        if op == '0':
            limpar_terminal()
            if meu_navio and len(meu_navio.tripulacao) > 0:
                if meu_navio.vida <= 0:
                    print("O seu navio está destruído! Repare-o ou crie um novo antes de zarpar.")
                else:
                    sim = Simulacao(meu_navio)
                    sim.jogar()
            else:
                print("Precisa de um navio e pelo menos um tripulante para iniciar a simulação.")
            input("\nPressione ENTER para continuar...")

        elif op == '1':
            limpar_terminal()
            nome = input("Nome do Navio: ")
            meu_navio = Navio(nome)
            print(f"Navio {nome} pronto para navegar.")
            input("Pressione ENTER para continuar...")

        elif op == '2':
            limpar_terminal()
            if meu_navio is None:
                print("Crie um navio primeiro.")
                input("Pressione ENTER para continuar...")
                continue
                
            print("\nEscolha a classe do tripulante:")
            print("1 - Espadachim")
            print("2 - Navegador")
            print("3 - Médico")
            print("4 - Cozinheiro")
            opcao_funcao = input("Escolha (número): ").strip()

            try:
                nome = input("Nome: ")
                recompensa = float(input("Bounty (M): "))
                poder = int(input("Poder (0-100): "))
                energia = int(input("Energia (0-100): "))

                novo_tripulante = None

                if opcao_funcao == '1':
                    espadas_str = input("Nomes das espadas (separados por vírgula): ")
                    espadas = [e.strip() for e in espadas_str.split(",") if e.strip()]
                    novo_tripulante = Espadachim(nome, recompensa, poder, espadas, energia)
                elif opcao_funcao == '2':
                    novo_tripulante = Navegador(nome, recompensa, poder, 0, energia)
                elif opcao_funcao == '3':
                    novo_tripulante = Medico(nome, recompensa, poder, 0, energia)
                elif opcao_funcao == '4':
                    novo_tripulante = Cozinheiro(nome, recompensa, poder, 0, energia)
                else:
                    print("Classe inválida. Recrutamento cancelado.")
                    input("Pressione ENTER para continuar...")
                    continue

                if meu_navio.recrutar(novo_tripulante):
                    print(f"{nome} foi recrutado com sucesso!")
            except ValueError as e:
                print(f"Erro nos dados: {e}")
            input("Pressione ENTER para continuar...")

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
                        else:
                            print("Tripulante não encontrado.")
                    else:
                        print("Escolha inválida.")
                except ValueError:
                    print("Entrada inválida.")
            input("\nPressione ENTER para continuar...")

        elif op == '4':
            limpar_terminal()
            if meu_navio:
                meu_navio.mostrar_manifesto()
                input("\nPressione ENTER para continuar...")

            else:
                print("Sem navio, sem manifesto.")
                input("\nPressione ENTER para continuar...")

        elif op == '5':
            limpar_terminal()
            if meu_navio:
                meu_navio.salvar()
            else:
                print("Nenhum navio para salvar.")
            input("\nPressione ENTER para continuar...")
            
        elif op == '6':
            limpar_terminal()
            carregado = carregar_navio()
            if carregado:
                meu_navio = carregado
            else:            
                print("Falha ao carregar navio.")
            input("\nPressione ENTER para continuar...")

        elif op == '7':
            limpar_terminal()
            meu_navio = criar_tripulacao_predefinida()
            print(f"Tripulação predefinida ({meu_navio.nome}) carregada com sucesso!")
            input("\nPressione ENTER para continuar...")

        elif op == '8':
            limpar_terminal()
            print("Rumo a Laugh Tale.\nAté a próxima aventura.")
            break

if __name__ == "__main__":
    main()

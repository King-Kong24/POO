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
from persistencia import salvar_jogo, carregar_jogo

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
        self.em_jogo = True

    def _imprimir_lento(self, texto, delay=0.01):
        """Imprime texto com um pequeno delay para efeito dramático (opcional)."""
        print(texto)
        # sys.stdout.flush()
        # time.sleep(delay) # Descomentar para efeito "typewriter"

    def _cabecalho(self):
        print(f"\n{'='*60}")
        print(f"  TURNO {self.turno_atual}/{self.MAX_TURNOS}")
        print(f"{'='*60}\n")

    def _mostrar_status_geral(self):
        self.navio.mostrar_manifesto()
        print()

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
            self._imprimir_lento(f"  ✅ SUCESSO! {tripulante.nome} sabia exatamente o que fazer.")
            ganho = evento.recompensa
            if ganho > 0:
                print(f"  💰 Tesouro obtido: {ganho} berry!")
                self.navio.ganhar_ouro(ganho)
            else:
                print("  O navio está seguro... por agora.")
        else:
            self._imprimir_lento(f"  ❌ FALHA! {tripulante.nome} tentou, mas não era a pessoa certa...")
            print(f"  💥 O navio sofre {evento.dano_vida} de dano!")
            self.navio.danificar(evento.dano_vida)
            
            if evento.dano_energia > 0:
                print(f"  😓 A tripulação perde {evento.dano_energia} de energia.")
                for t in self.navio.tripulacao:
                    t.trabalhar(evento.dano_energia / 5) # Conversão aproximada

    def jogar(self):
        print("\n\n")
        print("ONE PIECE: GRAND LINE ADVENTURES (PARTE 2)")
        print("  Sobrevivam à Grand Line e acumulem o maior tesouro!")
        print("\n")

        for i in range(1, self.MAX_TURNOS + 1):
            self.turno_atual = i
            self._cabecalho()
            self._mostrar_status_geral()

            # Verificar Game Over antes do turno
            if self.navio.vida <= 0:
                print("  💀 O navio foi destruído! Game Over.")
                break
            
            # Sorteio do Evento
            evento = random.choice(self.EVENTOS)
            print(f"  🎲 EVENTO: {evento.nome}")
            print(f"     \"{evento.descricao}\"")
            print(f"     (Ideal: {evento.tipo_ideal})\n")

            tripulante = self._escolher_tripulante()
            if not tripulante:
                print("  💤 Toda a tripulação está exausta! O navio fica à deriva...")
                self.navio.danificar(evento.dano_vida)
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


def criar_tripulacao():
    return [
        Espadachim("Zoro", recompensa=320.0, poder=90, espadas=["Wado", "Enma"]),
        Navegador("Nami", recompensa=66.0, poder=40, milhas_navegadas=1000),
        Medico("Chopper", recompensa=0.1, poder=30, pacientes_curados=50),
        Cozinheiro("Sanji", recompensa=330.0, poder=85, refeicoes_preparadas=500),
    ]

def main():
    navio = Navio("Going Merry 2.0")
    for t in criar_tripulacao():
        navio.recrutar(t)
    
    sim = Simulacao(navio)
    sim.jogar()

if __name__ == "__main__":
    main()

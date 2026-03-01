from persistencia import salvar_navio, carregar_navio
from colorama import Fore, Style

class navio:
    def __init__(self, nome, tripulacao=None):
       
        self.__nome = nome
        self.__tripulacao = []

    @property
    def nome(self):
      
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = str(nome)

    @property
    def tripulacao(self):
        
        return self.__tripulacao
    
    @tripulacao.setter
    def tripulacao(self, tripulacao):
      
        self.__tripulacao = list(tripulacao)
    
    @property
    def recompensa_total(self):
        
        return sum(t.recompensa for t in self.__tripulacao) 

    def recrutar(self, novo_tripulante):
        
        if any(t.nome.lower() == novo_tripulante.nome.lower() for t in self.__tripulacao):
            print(f"Erro: Já existe um tripulante chamado {novo_tripulante.nome}!")
            return False
        self.__tripulacao.append(novo_tripulante)
        return True
                                 
    def expulsar(self, nome_tripulante):
        
        tamanho_inicial = len(self.__tripulacao)
        self.__tripulacao = [t for t in self.__tripulacao if t.nome.lower() != nome_tripulante.lower()]
        return len(self.__tripulacao) < tamanho_inicial
    
    def calcular_poder_total(self):
        
        return sum(t.poder for t in self.__tripulacao)
        
    def mostrar_manifesto(self):
        tripulacao_ordenada = sorted(self.__tripulacao, reverse=True)

        print(f"{Fore.CYAN}{'=' * 30}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}MANIFESTO DO NAVIO: {self.nome.upper()}")
        print(f"{Fore.CYAN}{'=' * 30}")
        
        if not tripulacao_ordenada:
            print(f"{Fore.WHITE}Nenhum tripulante a bordo.")
            input(f"\nPressione {Fore.MAGENTA}ENTER{Style.RESET_ALL} para voltar ao menu...")
            return
        else:
            for t in tripulacao_ordenada:
                print(f"{t}")
                
            print(f"{Fore.CYAN}{'-'*30}")
            print(f"Poder Total: {Fore.RED}{self.calcular_poder_total()}")
            print(f"Recompensa Total: {Fore.GREEN}฿ {self.recompensa_total:,.0f}")
            
            print(Style.RESET_ALL)
            input(f"\nPressione {Fore.MAGENTA}ENTER{Style.RESET_ALL} para voltar ao menu...")

    def salvar(self):
        
        return salvar_navio(self)

    def carregar(cls, nome_navio=None):

        return carregar_navio(nome_navio)

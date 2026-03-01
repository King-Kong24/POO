from persistencia import salvar_navio, carregar_navio
from colorama import Fore, Style

class Navio:
    def __init__(self, nome, tripulacao=None):
       
        self.__nome = nome
        self.__tripulacao = []
        self.vida = 100
        self.ouro = 0


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
    def vida(self):
        return self.__vida
    
    @vida.setter
    def vida(self, vida):
        self.__vida = max(0, min(100, int(vida)))  

    @property
    def ouro(self):
        return self.__ouro
    
    @ouro.setter
    def ouro(self, ouro):
        self.__ouro = max(0, int(ouro))
    
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
    
    def reparar(self, quantidade):
        
        self.vida += quantidade

    def danificar(self, quantidade):
        self.vida -= quantidade

    def ganhar_ouro(self, quantidade):
        self.ouro += quantidade
        
    def mostrar_manifesto(self):
        tripulacao_ordenada = sorted(self.__tripulacao, reverse=True)

        print(f"{Fore.CYAN}{'=' * 30}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}MANIFESTO DO NAVIO: {self.nome}")
        print(f"{Fore.CYAN}{'=' * 30}")
        
        if not tripulacao_ordenada:
            print(f"{Fore.WHITE}Nenhum tripulante a bordo.")
        else:
            for t in tripulacao_ordenada:
                print(f"{t}")

            print(f"{Fore.CYAN}{'-'*30}")
            print(f"Vida do Navio: {Fore.RED}{self.vida}%")
            print(f"Ouro: {Fore.YELLOW} {self.ouro}")
            print(f"Poder Total: {Fore.RED}{self.calcular_poder_total()}")
            print(f"Recompensa Total: {Fore.GREEN} {self.recompensa_total:,.0f}")
            
            print(Style.RESET_ALL)

    def salvar(self):
        
        return salvar_navio(self)

    @classmethod
    def carregar(cls, nome_navio=None):

        return carregar_navio(nome_navio)

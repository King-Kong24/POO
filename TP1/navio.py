from persistencia import salvar_navio, carregar_navio

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
        
        print("-" * 30)
        print(f"MANIFESTO DO NAVIO: {self.nome}")
        print(f"Poder Total: {self.calcular_poder_total()}")
        print(f"Recompensa Total: {self.recompensa_total}")
        print("-" * 30)
        if not self.__tripulacao:
            print("Navio sem tripulação")
        for t in self.__tripulacao:    
            print(t)
        print("-" * 30)

    def salvar(self):
        
        return salvar_navio(self)

    def carregar(cls, nome_navio=None):

        return carregar_navio(nome_navio)

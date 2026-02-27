from tripulante import tripulante

class navio:
    def __init__(self, nome, tripulação=None):
        self.__nome = nome
        self.__tripulação = tripulação if tripulação is not None else []

    @property
    def nome(self):
        return self.__nome

    @property
    def tripulação(self):
        return self.__tripulação

    @property
    def recompensa_total(self):
        return sum(t.recompensa for t in self.__tripulação) 

    
    @nome.setter
    def nome(self, nome):
        self.__nome = str(nome)

    @tripulação.setter
    def tripulação(self, tripulação):
        self.__tripulação = list(tripulação)
    
    def recrutar(self, novo_tripulante):
        self.__tripulação.append(novo_tripulante)
                                 
    def expulsar(self, nome_tripulante):
        self.__tripulação = [t for t in self.__tripulação if t.nome != nome_tripulante]

    def calcular_poder_total(self):
        return sum(t.poder for t in self.__tripulação)
        
    def mostrar_manifesto(self):
        print(f"Manifesto do Navio {self.__nome}:")
        for t in self.__tripulação:    
            t.recompensa = float(t.recompensa) * 1000000
            print(f"Tripulante: {t.nome}, Recompensa: {t.recompensa}M, Poder: {t.poder}")
        print(f"Total de tripulantes: {len(self.__tripulação)}, "
              f"Recompensa total: {self.recompensa_total}M, "
              f"Poder total: {self.calcular_poder_total()}")
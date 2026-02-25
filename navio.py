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
        self.__nome = nome

    @tripulação.setter
    def tripulação(self, tripulação):
        self.__tripulação = tripulação
    
    def recrutar(novo_tripulante):
        self.__tripulação.append(novo_tripulante)
                                 
    def expulsar(nome_tripulante):
        self.__tripulação = [t for t in self.__tripulação if t.nome != nome_tripulante]

    def calcular_poder_total(self):
        return sum(t.poder for t in self.__tripulação)
        
    def mostrar_manifesto(self):
        print(f"Manifesto do Navio {self.__nome}:")
        for t in self.__tripulação:
            print(t)
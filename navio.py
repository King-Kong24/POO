from tripulante import tripulante

class navio:
    def __init__(self, nome, tripulação=None):
        self.__nome = nome
        self.__tripulação = tripulação if tripulação is not None else []

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter


    @property
    def tripulação(self):
        return self.__tripulação
    
    @tripulação.setter
    def

    @property
    def recompensa_total(self):
        return sum(t.recompensa for t in self.__tripulação)
    
    def recrutar(novo_tripulante):
        self.__tripulação.append(novo_tripulante)
                                 
    def expulsar(nome_tripulante):
        self.__tripulação = [t for t in self.__tripulação if t.nome != nome_tripulante]

    def calcular_poder_total():
        
        
    def mostrar_manifesto():
        pass
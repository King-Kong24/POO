class tripulante:
    def __init__(self, nome, funcao, recompensa, poder, energia):
        self.__nome = nome
        self.__funcao = funcao
        self.__recompensa = recompensa
        self.__poder = poder
        self.__energia = energia

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def funcao(self):
        return self.__funcao
    
    @funcao.setter
    def funcao(self, funcao):
        self.__funcao = funcao

    @property
    def recompensa(self):
        return self.__recompensa
    
    @recompensa.setter
    def recompensa(self, recompensa):
        self.__recompensa = recompensa

    @property
    def poder(self):
        return self.__poder
    
    @poder.setter
    def poder(self, poder):
        self.__poder = poder


    @property
    def energia(self):
        return self.__energia

    @energia.setter
    def energia(self, energia):
        self.__energia = energia

    def trabalhar(tempo):
        self.__energia -= tempo * 5
        if self.__energia < 0:
            self.__energia = 0
    
    def descansar(self, tempo):
        self.__energia += tempo * 10
        if self.__energia > 100:
            self.__energia = 100
    
    def __str__(self):
        return f"Tripulante: {self.__nome}, Função: {self.__funcao}, Recompensa: {self.__recompensa}, Poder: {self.__poder}, Energia: {self.__energia}"
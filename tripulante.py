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
    
    @property
    def funcao(self):
        return self.__funcao
    
    @property
    def recompensa(self):
        return self.__recompensa
    

    @property
    def poder(self):
        return self.__poder

    @property
    def energia(self):
        return self.__energia
    
    @nome.setter
    def nome(self, nome):
        self.__nome = nome    

    @funcao.setter
    def funcao(self, funcao):
        self.__funcao = funcao
    
    @recompensa.setter
    def recompensa(self, recompensa):
        self.__recompensa = recompensa
        if recompensa < 0:
            print("Erro: Recompensa não pode ser negativa.")

    @poder.setter
    def poder(self, poder):
        self.__poder = poder
        if poder < 0:
            print("Erro: Poder não pode ser negativo.")
        if poder > 100:
            print("Erro: Poder não pode ser maior que 100.")

    @energia.setter
    def energia(self, energia):
        self.__energia = energia
        if energia < 0:
            print
        if energia > 100:
            print("Erro: Energia não pode ser maior que 100.")

    def trabalhar(tempo):
        self.__energia -= tempo * 5
        if self.__energia < 0:
            print("Erro: Energia insuficiente para trabalhar.")
    
    def descansar(self, tempo):
        self.__energia += tempo * 10
        if self.__energia > 100:
            self.__energia = 100
    
    def __str__(self):
        return f"Tripulante: {self.__nome}, Função: {self.__funcao}, Recompensa: {self.__recompensa}, Poder: {self.__poder}, Energia: {self.__energia}"
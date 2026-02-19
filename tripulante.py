class tripulante:
    def __init__(self, nome, funcao, recompensa, poder, energia):
        self.__nome = nome
        self.__funcao = funcao
        self.__recompensa = recompensa
        self.__poder = poder
        self.__energia = energia

    def trabalhar(tempo):
        self.__energia -= tempo * 5
        if self.__energia < 0:
            self.__energia = 0
    
    def descansar():
        
        if self.__energia > 100:
            self.__energia = 100

    def __str__(self):
        return f"Tripulante: {self.__nome}, Função: {self.__funcao}, Recompensa: {self.__recompensa}, Poder: {self.__poder}, Energia: {self.__energia}"
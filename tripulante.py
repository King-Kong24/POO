class tripulante:
    def __init__(self, nome, funcao, recompensa, poder, energia):
        self.nome = nome
        self.funcao = funcao
        self.recompensa = recompensa
        self.poder = poder
        self.energia = energia

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome):
        self.__nome = str(nome)

    @property
    def funcao(self):
        return self.__funcao

    @funcao.setter
    def funcao(self, funcao):
        self.__funcao = str(funcao)
    
    @property
    def recompensa(self):
        return self.__recompensa
    
    @recompensa.setter
    def recompensa(self, recompensa):
        if recompensa < 0:
            raise ValueError("Erro: Recompensa não pode ser negativa.")
        self.__recompensa = float(recompensa)

    @property
    def poder(self):
        return self.__poder

    @poder.setter
    def poder(self, poder):
        if not (0 <= poder <= 100):
            print("Erro: Poder deve estar entre 0 e 100.")
            return  # Return early to avoid setting invalid power
        self.__poder = int(poder)

    @property
    def energia(self):
        return self.__energia

    @energia.setter
    def energia(self, energia):
        if energia < 0:
            print("Erro: Energia não pode ser negativa.")
            return  # Return early to avoid setting negative energy
        elif energia > 100:
            self.__energia = 100
        else:
            self.__energia = int(energia)

    def trabalhar(self, tempo):
        self.__energia -= tempo * 5
        if self.__energia <= 0:
            print("Erro: Energia insuficiente para trabalhar.")
    
    def descansar(self, tempo):
        self.__energia += tempo * 10
        if self.__energia > 100:
            self.__energia = 100
    def __str__(self):
        recompensa_formatada = self.__recompensa / 1000000
        return f"Tripulante: {self.__nome}, Função: {self.__funcao}, Recompensa: {recompensa_formatada}M, Poder: {self.__poder}, Energia: {self.__energia}"
    
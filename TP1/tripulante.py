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
            self.__recompensa = 0.0
        else:
            self.__recompensa = float(recompensa)

    @property
    def poder(self):
        return self.__poder

    @poder.setter
    def poder(self, poder):
        if poder < 0:
            self.__poder = 0
        elif poder > 100:
            self.__poder = 100
        else:
            self.__poder = int(poder)

    @property
    def energia(self):
        return self.__energia

    @energia.setter
    def energia(self, energia):
        if energia < 0:
            self.__energia = 0
        elif energia > 100:
            self.__energia = 100
        else:
            self.__energia = int(energia)

    def trabalhar(self, tempo):
        self.__energia -= tempo * 5
        if self.__energia <= 0:
            self.__energia = 0
            print(f"{self.nome} está exausto e não pode trabalhar mais")
            
    def descansar(self, tempo):
        self.__energia = 100

    def __str__(self):
        rec_formatada = self.__recompensa / 1000000
        return f"Tripulante: {self.__nome}, Função: {self.__funcao}, Bounty: {rec_formatada:.0f}M, Poder: {self.__poder}, Energia: {self.__energia}"

    def __lt__(self, outro):
        return self.poder < outro.poder
    
    def to_dict(self):
        return {
            "nome": self.__nome,
            "funcao": self.__funcao,
            "recompensa": self.__recompensa,
            "poder": self.__poder,
            "energia": self.__energia
        }
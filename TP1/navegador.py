from tripulante import Tripulante

class Navegador(Tripulante):
    def __init__(self, nome, recompensa=0.0, poder=0, milhas_navegadas=0, energia=100):
       
        super().__init__(nome, recompensa, poder, energia)
        self.milhas_navegadas = milhas_navegadas

    @property
    def milhas_navegadas(self):
       
        return self.__milhas_navegadas

    @milhas_navegadas.setter
    def milhas_navegadas(self, valor):
       
        self.__milhas_navegadas = max(0, int(valor))

    def executar_acao(self, navio):
        
        self.milhas_navegadas += 50
        print(f"{self.nome} leu as correntes e traçou uma nova rota segura. Milhas navegadas aumentaram para {self.milhas_navegadas}.")

    def __str__(self):
        
        return f"{super().__str__()} | Milhas: {self.milhas_navegadas}"
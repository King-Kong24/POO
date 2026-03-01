from tripulante import Tripulante

class Cozinheiro(Tripulante):
    def __init__(self, nome, recompensa=0.0, poder=0, refeicoes_preparadas=0, energia=100):
       
        super().__init__(nome, recompensa, poder, energia)
        self.refeicoes_preparadas = refeicoes_preparadas

    @property
    def refeicoes_preparadas(self):
      
        return self.__refeicoes_preparadas

    @refeicoes_preparadas.setter
    def refeicoes_preparadas(self, valor):
      
        self.__refeicoes_preparadas = max(0, int(valor))

    def executar_acao(self, navio):
      
        if not navio.tripulacao:
            return

        for membro in navio.tripulacao:
            membro.energia += 20
        self.refeicoes_preparadas += 1
        print(f"{self.nome} cozinhou um banquete formidável. Toda a tripulação recuperou energia.")

    def __str__(self):
        
        return f"{super().__str__()} | Refeições: {self.refeicoes_preparadas}"
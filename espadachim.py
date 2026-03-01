from tripulante import Tripulante

class Espadachim(Tripulante):
    def __init__(self, nome, recompensa=0.0, poder=0, espadas=None, energia=100):
        """Inicializa um novo espadachim.
        
        Args:
            nome: Nome do espadachim.
            recompensa: Valor da recompensa em ouro (bounty).
            poder: Poder de combate do espadachim (0-100).
            espadas: Lista de nomes das espadas que o espadachim possui.
            energia: Nível de energia inicial (0-100).
        """
        super().__init__(nome, recompensa, poder, energia)
        self.espadas = espadas if espadas is not None else []

    @property
    def espadas(self):
      
        return self.__espadas

    @espadas.setter
    def espadas(self, valor):
      
        self.__espadas = list(valor)

    def executar_acao(self, navio):
      
        bonus = 10 * len(self.espadas)
        self.poder += bonus
        print(f"{self.nome} executa um ataque devastador com as suas {len(self.espadas)} espadas. Ganhou +{bonus} de poder temporário.")

    def __str__(self):
      
        base = super().__str__()
        espadas_str = ", ".join(self.espadas) if self.espadas else "Nenhuma"
        return f"{base} | Espadas: {espadas_str}"
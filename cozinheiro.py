from tripulante import Tripulante

class Cozinheiro(Tripulante):
    # O cozinheiro é responsável por preparar refeições que recuperam a energia da tripulação.
    def __init__(self, nome, recompensa=0.0, poder=0, refeicoes_preparadas=0, energia=100):
        """Inicializa um novo cozinheiro.
        
        Args:
            nome: Nome do cozinheiro.
            recompensa: Valor da recompensa em ouro (bounty).
            poder: Poder de combate do cozinheiro (0-100).
            refeicoes_preparadas: Número inicial de refeições preparadas.
            energia: Nível de energia inicial (0-100).
        """
        super().__init__(nome, recompensa, poder, energia)
        self.refeicoes_preparadas = refeicoes_preparadas

    @property
    def refeicoes_preparadas(self):
        # Devolve o número de refeições preparadas pelo cozinheiro.
        return self.__refeicoes_preparadas

    @refeicoes_preparadas.setter
    def refeicoes_preparadas(self, valor):
        # Garante que o número de refeições preparadas seja sempre um valor inteiro não negativo.
        self.__refeicoes_preparadas = max(0, int(valor))

    def executar_acao(self, navio):
        # O cozinheiro prepara uma refeição que recupera a energia de toda a tripulação. O número de refeições preparadas é incrementado.
        if not navio.tripulacao:
            return

        for membro in navio.tripulacao:
            membro.energia += 20
        self.refeicoes_preparadas += 1
        print(f"{self.nome} cozinhou um banquete formidável. Toda a tripulação recuperou energia.")

    def __str__(self):
        # Representação visual do cozinheiro, incluindo o número de refeições preparadas.
        return f"{super().__str__()} | Refeições: {self.refeicoes_preparadas}"
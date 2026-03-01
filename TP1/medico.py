from tripulante import Tripulante

class Medico(Tripulante):
    def __init__(self, nome, recompensa=0.0, poder=0, pacientes_curados=0, energia=100):
      
        super().__init__(nome, recompensa, poder, energia)
        self.pacientes_curados = pacientes_curados

    @property
    def pacientes_curados(self):
       
        return self.__pacientes_curados

    @pacientes_curados.setter
    def pacientes_curados(self, valor):
       
        self.__pacientes_curados = max(0, int(valor))

    def executar_acao(self, navio):
        
        if not navio.tripulacao:
            print(f"🩺 {self.nome} preparou ligaduras, mas não há ninguém a bordo!")
            return
        paciente = min(navio.tripulacao, key=lambda t: t.energia)
        paciente.energia += 40
        self.pacientes_curados += 1
        print(f"{self.nome} tratou as feridas de {paciente.nome}. Energia de {paciente.nome} recuperada. Total curados: {self.pacientes_curados}.")

    def __str__(self):
       
        return f"{super().__str__()} | Curados: {self.pacientes_curados}"
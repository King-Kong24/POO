from colorama import Fore, Style

class Tripulante:
    # Define a estrutura básica de um tripulante
    def __init__(self, nome, recompensa=0.0, poder=0, energia=100):
        # Inicializa os atributos do tripulante
        self.nome = nome
        self.recompensa = recompensa
        self.poder = poder
        self.energia = energia
        self.status = "Ok"

    @property
    def nome(self):
        # Devolve o nome do tripulante
        return self.__nome
    
    @nome.setter
    def nome(self, nome):
        # Garantir que o nome seja sempre uma string
        self.__nome = str(nome)

    @property
    def recompensa(self):
        # Devolve a recompensa do tripulante
        return self.__recompensa
    
    @recompensa.setter
    def recompensa(self, recompensa):
        # Garantir que a recompensa seja sempre um valor float não negativo
        self.__recompensa = max(0.0, float(recompensa))

    @property
    def poder(self):
        # Devolve o poder do tripulante
        return self.__poder

    @poder.setter
    def poder(self, poder):
        # Garantir que o poder esteja entre 0 e 100
        self.__poder = max(0, min(100, int(poder)))

    @property
    def energia(self):
        # Devolve a energia atual do tripulante
        return self.__energia

    @energia.setter
    def energia(self, energia):
        # Garantir que a energia esteja entre 0 e 100
        self.__energia = max(0, min(100, int(energia)))

    @property
    def status(self):
        # Devolve o status do tripulante
        return self.__status
    
    @status.setter
    def status(self, status):
        # Garantir que o status seja sempre uma string
        self.__status = str(status)

    def executar_acao(self, navio):
        # Método genérico para ser sobrescrito por subclasses específicas de tripulantes
        print(f"{self.nome} não sabe bem o que fazer nesta situação...")    
    
    def __lt__(self, outro):
        # Define a comparação entre tripulantes com base no poder e recompensa
        if not isinstance(outro, Tripulante):
            return NotImplemented
        if self.poder != outro.poder:
            return self.poder < outro.poder
        return self.recompensa < outro.recompensa

    def trabalhar(self, tempo):
        # Simula o trabalho do tripulante, reduzindo sua energia com base no tempo trabalhado
        self.__energia -= tempo * 5
        if self.__energia <= 0:
            self.__energia = 0
            self.status = "Morto"
            print(f"{Fore.RED}💀 {self.nome} não resistiu à exaustão e desfaleceu.{Style.RESET_ALL}")
            
    def descansar(self):
        # Simula o descanso do tripulante, recuperando sua energia
        self.__energia = 100

    def __str__(self):
        # Representação visual do tripulante, incluindo barras de energia e cores para status
        barras = int(self.__energia / 10)
        cor_energia = Fore.YELLOW if self.__energia > 50 else Fore.RED
        barra_vis = f"[{cor_energia}{'#' * barras}{Fore.WHITE}{'.' * (10 - barras)}]"
        nome_funcao = type(self).__name__
        cor_funcao = Fore.RED if nome_funcao == "Capitao" else Fore.WHITE
        cor_status = Fore.GREEN if self.status == "Ok" else Fore.RED
        
        return f"{Fore.WHITE}Nome: {self.nome:12} | {cor_funcao}Função: {nome_funcao:12} {Style.RESET_ALL}| Status: {cor_status}{self.status:8} {Style.RESET_ALL}| {Fore.GREEN}Poder: {self.poder:3} {Style.RESET_ALL}| {Fore.BLUE}Recompensa: {self.recompensa:.0f}M {Style.RESET_ALL}| Energia: {barra_vis} {self.energia}%"

    def to_dict(self):
        # Converte o tripulante em um dicionário para facilitar a serialização
        return {
            "nome": self.__nome,
            "recompensa": self.__recompensa,
            "poder": self.__poder,
            "energia": self.__energia,
            "status": self.__status
        }
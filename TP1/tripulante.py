from colorama import Fore, Style

class Tripulante:
   
    def __init__(self, nome, recompensa=0.0, poder=0, energia=100):
      
        self.nome = nome
        self.recompensa = recompensa
        self.poder = poder
        self.energia = energia
        self.status = "Ok"

    @property
    def nome(self):
        
        return self.__nome
    
    @nome.setter
    def nome(self, nome):
      
        self.__nome = str(nome)

    @property
    def recompensa(self):
       
        return self.__recompensa
    
    @recompensa.setter
    def recompensa(self, recompensa):
 
        self.__recompensa = max(0.0, float(recompensa))

    @property
    def poder(self):
        
        return self.__poder

    @poder.setter
    def poder(self, poder):
      
        self.__poder = max(0, min(100, int(poder)))

    @property
    def energia(self):
       
        return self.__energia

    @energia.setter
    def energia(self, energia):
       
        self.__energia = max(0, min(100, int(energia)))

    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, status):
        self.__status = str(status)

    def executar_acao(self, navio):

        print(f"{self.nome} não sabe bem o que fazer nesta situação...")    
    
    def __lt__(self, outro):
        
        if not isinstance(outro, Tripulante):
            return NotImplemented
        if self.poder != outro.poder:
            return self.poder < outro.poder
        return self.recompensa < outro.recompensa

    def trabalhar(self, tempo):
        
        self.__energia -= tempo * 5
        if self.__energia <= 0:
            self.__energia = 0
            print(f"{self.nome} está exausto.")
            
    def descansar(self):
       
        self.__energia = 100

    def __str__(self):
        
        barras = int(self.__energia / 10)
        cor_energia = Fore.YELLOW if self.__energia > 50 else Fore.RED
        barra_vis = f"[{cor_energia}{'#' * barras}{Fore.WHITE}{'.' * (10 - barras)}]"
        nome_funcao = type(self).__name__
        cor_funcao = Fore.RED if nome_funcao == "Capitao" else Fore.WHITE
        
        return f"{Fore.WHITE}Nome: {self.nome:12} | {cor_funcao}Função: {nome_funcao:12} {Style.RESET_ALL}| Status: {self.status:8} | {Fore.GREEN}Poder: {self.poder:3} {Style.RESET_ALL}| {Fore.BLUE}Recompensa: {self.recompensa:.0f}M {Style.RESET_ALL}| Energia: {barra_vis} {self.energia}%"

    def to_dict(self):

        return {
            "nome": self.__nome,
            "recompensa": self.__recompensa,
            "poder": self.__poder,
            "energia": self.__energia,
            "status": self.__status
        }
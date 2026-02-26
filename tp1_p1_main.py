from tripulante import tripulante
from navio import navio

def main():
    # Criando tripulantes
    tripulante1 = tripulante("Luffy", "Capitão", 1500000000, 90, 100)
    tripulante2 = tripulante("Zoro", "Espadachim", 320000000, 85, 95)
    tripulante3 = tripulante("Nami", "Navegadora", 66000000, 70, 80)

    # Criando navio e recrutando tripulantes
    navio1 = navio("Thousand Sunny")
    navio1.recrutar(tripulante1)
    navio1.recrutar(tripulante2)
    navio1.recrutar(tripulante3)

    # Exibindo manifesto do navio
    navio1.mostrar_manifesto()
    
if __name__ == "__main__":
    main()
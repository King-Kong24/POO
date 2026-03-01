import json
from tripulante import Tripulante
from espadachim import Espadachim
from navegador import Navegador
from medico import Medico
from cozinheiro import Cozinheiro
import navio as navio_class
import os
# Define o caminho do ficheiro.
arquivo_save = os.path.join(os.path.dirname(__file__), "save.json")

def ler_arquivo():
    # Lê o conteúdo do ficheiro de gravação e retorna um dicionário. Se o ficheiro não existir ou estiver vazio, retorna um dicionário vazio.
    if not os.path.exists(arquivo_save):
        return {}
    with open(arquivo_save, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {}

def salvar_navio(navio_obj):
    # Salva o estado do navio e sua tripulação no ficheiro de gravação, organizando os dados em um formato estruturado para facilitar a leitura e posterior carregamento.
    geral = ler_arquivo()
    tripulacao_formatada = []
    for t in navio_obj.tripulacao:
        dados_t = {
            "tipo": type(t).__name__,
            "nome": t.nome,
            "recompensa": t.recompensa,
            "poder": t.poder,
            "energia": t.energia,
           "status": t.status
        }
        
    if isinstance(t, Espadachim):
        dados_t["espadas"] = t.espadas
    elif isinstance(t, Navegador):
        dados_t["milhas_navegadas"] = t.milhas_navegadas
    elif isinstance(t, Medico):
        dados_t["pacientes_curados"] = t.pacientes_curados
    elif isinstance(t, Cozinheiro):
        dados_t["refeicoes_preparadas"] = t.refeicoes_preparadas
            
    tripulacao_formatada.append(dados_t)
    
    dados_navio = {
        "nome_navio": navio_obj.nome,
        "vida": navio_obj.vida,
        "ouro": navio_obj.ouro,
        "tripulacao": tripulacao_formatada
    }
    geral[navio_obj.nome] = dados_navio

    with open(arquivo_save, "w", encoding="utf-8") as f:
        json.dump(geral, f, indent=4, ensure_ascii=False)
    print(f"Estado do navio '{navio_obj.nome}' guardado com sucesso!")

def carregar_navio(nome_navio=None):
    # Carrega o estado do navio e sua tripulação a partir do ficheiro de gravação, criando um objeto Navio com os dados recuperados. Se o nome do navio não for especificado, carrega o primeiro navio encontrado no ficheiro.
    geral = ler_arquivo()
    if not geral:
        print("Erro: Ficheiro de gravação não encontrado ou vazio.")
        return None

    if nome_navio is None:
        nome_navio = next(iter(geral))

    dados = geral.get(nome_navio)

    if dados is None:
        print(f"Erro: navio '{nome_navio}' não encontrado no ficheiro.")
        return None

    nav = navio_class.Navio(dados["nome_navio"])
    if "vida" in dados:
        nav.vida = dados["vida"]
    if "ouro" in dados:
        nav.ouro = dados["ouro"]

    for t_dados in dados.get("tripulacao", []):
        tipo = t_dados.get("tipo", "Tripulante")
        nome = t_dados["nome"]
        recompensa = t_dados["recompensa"]
        poder = t_dados["poder"]
        energia = t_dados.get("energia", 100)
        
        if tipo == "Espadachim":
            novo_t = Espadachim(nome, recompensa, poder, t_dados.get("espadas", []), energia)
        elif tipo == "Navegador":
            novo_t = Navegador(nome, recompensa, poder, t_dados.get("milhas_navegadas", 0), energia)
        elif tipo == "Medico":
            novo_t = Medico(nome, recompensa, poder, t_dados.get("pacientes_curados", 0), energia)
        elif tipo == "Cozinheiro":
            novo_t = Cozinheiro(nome, recompensa, poder, t_dados.get("refeicoes_preparadas", 0), energia)
        else:
            novo_t = Tripulante(nome, recompensa, poder, energia)
            
        if "status" in t_dados:
            novo_t.status = t_dados["status"]
        nav.recrutar(novo_t)
    print(f"Navio '{nav.nome}' carregado com sucesso.")
    return nav

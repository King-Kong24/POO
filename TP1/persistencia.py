import json
from tripulante import tripulante
import navio as navio_class
import os

arquivo_save = os.path.join(os.path.dirname(__file__), "save.json")

def ler_arquivo():
    if not os.path.exists(arquivo_save):
        return {}
    with open(arquivo_save, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {}

def salvar_navio(navio_obj):

    geral = ler_arquivo()
    dados_navio = {
        "nome_navio": navio_obj.nome,
        "tripulacao": [
            {
                "nome": t.nome,
                "funcao": t.funcao,
                "recompensa": t.recompensa,
                "poder": t.poder,
                "energia": t.energia,
            }
            for t in navio_obj.tripulacao
        ],
    }
    geral[navio_obj.nome] = dados_navio

    with open(arquivo_save, "w", encoding="utf-8") as f:
        json.dump(geral, f, indent=4, ensure_ascii=False)
    print(f"Estado do navio '{navio_obj.nome}' guardado com sucesso!")

def carregar_navio(nome_navio=None):

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

    nav = navio_class.navio(dados["nome_navio"])
    for t_dados in dados["tripulacao"]:
        novo_t = tripulante(
            t_dados["nome"],
            t_dados["funcao"],
            t_dados["recompensa"],
            t_dados["poder"],
            t_dados["energia"],
        )
        nav.recrutar(novo_t)
    print(f"Navio '{nav.nome}' carregado com sucesso.")
    return nav

#uvx pytest test_tp1_check.py -v
# /// script
# requires-python = ">=3.10"
# dependencies = ["pytest"]
# ///
"""Testes pytest para verificar as classes do TP1 (Partes 1 e 2)."""

import pytest

from navio import Navio
from tripulante import Tripulante
from espadachim import Espadachim
from navegador import Navegador
from medico import Medico
from cozinheiro import Cozinheiro


# ── Fixtures ────────────────────────────────────────────────────── #
@pytest.fixture
def navio():
    return Navio("Going Merry 2.0")


@pytest.fixture
def tripulacao():
    return [
        Espadachim("Zoro", recompensa=320.0, poder=90, espadas=["Wado", "Enma"]),
        Navegador("Nami", recompensa=66.0, poder=40, milhas_navegadas=1000),
        Medico("Chopper", recompensa=0.1, poder=30, pacientes_curados=50),
        Cozinheiro("Sanji", recompensa=330.0, poder=85, refeicoes_preparadas=500),
    ]


@pytest.fixture
def navio_com_tripulacao(navio, tripulacao):
    for t in tripulacao:
        navio.recrutar(t)
    return navio


# ── Tripulante ──────────────────────────────────────────────────── #

class TestTripulante:
    def test_criacao(self):
        t = Tripulante("Luffy", recompensa=1500.0, poder=95)
        assert t.nome == "Luffy"
        assert t.recompensa == 1500.0
        assert t.poder == 95
        assert t.energia == 100
        assert t.status == "Ok"

    def test_trabalhar_reduz_energia(self):
        t = Tripulante("Luffy")
        t.trabalhar(10)
        assert t.energia == 50  # 100 - 10*5

    def test_energia_nao_fica_negativa(self):
        t = Tripulante("Luffy")
        t.trabalhar(30)  # 100 - 30*5 = -50 → clamped to 0
        assert t.energia == 0

    def test_descansar_recupera_energia(self):
        t = Tripulante("Luffy")
        t.trabalhar(10)
        t.descansar()
        assert t.energia == 100

    def test_status_pode_ser_alterado(self):
        t = Tripulante("Luffy")
        t.status = "Ferido"
        assert t.status == "Ferido"

    def test_str(self):
        t = Tripulante("Luffy", recompensa=100.0, poder=50)
        s = str(t)
        assert "Luffy" in s
        assert "Tripulante" in s


# ── Navio ───────────────────────────────────────────────────────── #

class TestNavio:
    def test_criacao(self, navio):
        assert navio.nome == "Going Merry 2.0"
        assert navio.vida == 100
        assert navio.ouro == 0

    def test_recrutar(self, navio):
        t = Tripulante("Luffy")
        navio.recrutar(t)
        assert len(navio.tripulacao) == 1

    def test_expulsar_existente(self, navio_com_tripulacao):
        assert navio_com_tripulacao.expulsar("Nami") is True
        assert len(navio_com_tripulacao.tripulacao) == 3

    def test_expulsar_inexistente(self, navio_com_tripulacao):
        assert navio_com_tripulacao.expulsar("Fantasma") is False
        assert len(navio_com_tripulacao.tripulacao) == 4

    def test_danificar(self, navio):
        navio.danificar(30)
        assert navio.vida == 70

    def test_danificar_clamp_zero(self, navio):
        navio.danificar(150)
        assert navio.vida == 0

    def test_reparar(self, navio):
        navio.danificar(60)
        navio.reparar(30)
        assert navio.vida == 70

    def test_reparar_clamp_100(self, navio):
        navio.danificar(10)
        navio.reparar(50)
        assert navio.vida == 100

    def test_ganhar_ouro(self, navio):
        navio.ganhar_ouro(500)
        assert navio.ouro == 500

    def test_recompensa_total(self, navio_com_tripulacao):
        assert navio_com_tripulacao.recompensa_total == pytest.approx(716.1)

    def test_poder_total(self, navio_com_tripulacao):
        assert navio_com_tripulacao.calcular_poder_total() == 245

    def test_mostrar_manifesto(self, navio_com_tripulacao, capsys):
        navio_com_tripulacao.mostrar_manifesto()
        output = capsys.readouterr().out
        assert "Going Merry 2.0" in output
        assert "Zoro" in output


# ── Subclasses ──────────────────────────────────────────────────── #

class TestEspadachim:
    def test_heranca(self):
        z = Espadachim("Zoro", espadas=["Wado"])
        assert isinstance(z, Tripulante)

    def test_espadas(self):
        z = Espadachim("Zoro", espadas=["Wado", "Enma"])
        assert z.espadas == ["Wado", "Enma"]

    def test_executar_acao(self, navio_com_tripulacao, capsys):
        zoro = navio_com_tripulacao.tripulacao[0]
        zoro.executar_acao(navio_com_tripulacao)
        output = capsys.readouterr().out
        assert "Zoro" in output

    def test_str_inclui_espadas(self):
        z = Espadachim("Zoro", espadas=["Wado"])
        assert "Wado" in str(z)


class TestNavegador:
    def test_heranca(self):
        n = Navegador("Nami")
        assert isinstance(n, Tripulante)

    def test_milhas(self):
        n = Navegador("Nami", milhas_navegadas=1000)
        assert n.milhas_navegadas == 1000

    def test_executar_acao_incrementa_milhas(self, navio_com_tripulacao):
        nami = navio_com_tripulacao.tripulacao[1]
        milhas_antes = nami.milhas_navegadas
        nami.executar_acao(navio_com_tripulacao)
        assert nami.milhas_navegadas > milhas_antes


class TestMedico:
    def test_heranca(self):
        m = Medico("Chopper")
        assert isinstance(m, Tripulante)

    def test_executar_acao_cura(self, navio_com_tripulacao):
        chopper = navio_com_tripulacao.tripulacao[2]
        # Gastar energia de alguém primeiro
        navio_com_tripulacao.tripulacao[0].trabalhar(10)
        energia_antes = navio_com_tripulacao.tripulacao[0].energia
        curados_antes = chopper.pacientes_curados
        chopper.executar_acao(navio_com_tripulacao)
        assert chopper.pacientes_curados == curados_antes + 1


class TestCozinheiro:
    def test_heranca(self):
        c = Cozinheiro("Sanji")
        assert isinstance(c, Tripulante)

    def test_executar_acao_recupera_energia(self, navio_com_tripulacao):
        # Gastar energia de todos
        for t in navio_com_tripulacao.tripulacao:
            t.trabalhar(10)
        energias_antes = [t.energia for t in navio_com_tripulacao.tripulacao]
        sanji = navio_com_tripulacao.tripulacao[3]
        sanji.executar_acao(navio_com_tripulacao)
        for i, t in enumerate(navio_com_tripulacao.tripulacao):
            assert t.energia >= energias_antes[i]

    def test_refeicoes_incrementa(self, navio_com_tripulacao):
        sanji = navio_com_tripulacao.tripulacao[3]
        refeicoes_antes = sanji.refeicoes_preparadas
        sanji.executar_acao(navio_com_tripulacao)
        assert sanji.refeicoes_preparadas == refeicoes_antes + 1

# One Piece: Grand Line Adventures

Feito por João Medeiros - a94570 - LESTI

## Descrição do Projeto

**One Piece: Grand Line Adventures** é um simulador de gestão de tripulação pirata baseado no universo de One Piece. O projeto implementa conceitos fundamentais de **Programação Orientada a Objetos (POO)** em Python, incluindo herança, polimorfismo, encapsulamento e persistência de dados.

O projeto é dividido em duas partes:
- **Parte 1 (tp1_p1_main.py)**: Menu interativo básico para gestão de navio e tripulação
- **Parte 2 (tp1_p2_main.py)**: Simulação completa com eventos aleatórios, sistema de vida e recompensas

---

## Funcionalidades Principais

### Parte 1 - Gestão Básica
- Criar um novo navio
- Recrutar tripulantes
- Expulsar tripulantes
- Visualizar manifesto da tripulação
- Colocar tripulantes a trabalhar (reduz energia)
- Colocar tripulantes a descansar (recupera energia)
- Salvar estado do navio em JSON
- Carregar navio guardado

### Parte 2 - Simulação Completa
- Eventos aleatórios (Kraken, Tempestade, Escorbuto, etc.)
- Sistema de vida do navio
- Sistema de ouro/recompensas
- Polimorfismo: diferentes tripulantes resolvem eventos diferentemente
- Ranking e pontuação final

---

## Arquitetura do Projeto

### Diagrama de Classes

```
Tripulante (classe base)
    ├── Espadachim (especialista em combate)
    ├── Navegador (especialista em rotas)
    ├── Médico (especialista em cura)
    └── Cozinheiro (especialista em energia)

Navio (gerencia a tripulação)
    └── Persistencia (salva/carrega dados)
```

### Estrutura de Ficheiros

```
TP1/
├── tripulante.py          # Classe base Tripulante
├── espadachim.py          # Subclasse Espadachim
├── navegador.py           # Subclasse Navegador
├── medico.py              # Subclasse Medico
├── cozinheiro.py          # Subclasse Cozinheiro
├── navio.py               # Classe Navio
├── persistencia.py        # Funções de salvar/carregar
├── tp1_p1_main.py         # Menu Parte 1
├── tp1_p2_main.py         # Simulação Parte 2
├── test_tp1_check.py      # Testes unitários
├── save.json              # Ficheiro de gravação (auto-criado)
└── README.md              # Documentação original
```

---

## Documentação das Classes

### Classe `Tripulante` (Base)

**Descrição:** Representa um membro genérico da tripulação.

**Atributos:**
- `nome` (str): Nome do tripulante
- `recompensa` (float): Bounty em ouro (≥ 0)
- `poder` (int): Poder de combate (0-100)
- `energia` (int): Nível de energia (0-100)
- `status` (str): Estado atual ("Ok", "Ferido", "Morto")

**Métodos Principais:**
```python
# Reduz energia em função do tempo trabalhado
tripulante.trabalhar(tempo)

# Recupera energia para 100
tripulante.descansar()

# Executa ação especial (sobrescrito por subclasses)
tripulante.executar_acao(navio)

# Comparação entre tripulantes (por poder, depois recompensa)
tripulante1 < tripulante2
```

**Exemplo de Uso:**
```python
from tripulante import Tripulante

luffy = Tripulante("Luffy", recompensa=1500.0, poder=95, energia=100)
print(luffy.status)  # "Ok"
luffy.trabalhar(10)  # Energia: 100 - 10*5 = 50
luffy.descansar()    # Energia: 100
```

---

### Classe `Espadachim`

**Descrição:** Tripulante especializado em combate com múltiplas espadas.

**Atributos Especiais:**
- `espadas` (list): Lista de nomes das espadas que possui

**Método Especial:**
```python
# Aumenta o poder em 10 pontos por espada
# Imprime mensagem de ataque devastador
espadachim.executar_acao(navio)
```

**Exemplo:**
```python
from espadachim import Espadachim

zoro = Espadachim("Zoro", recompensa=320.0, poder=90, 
                  espadas=["Wado", "Enma", "Shusui"])
print(str(zoro))     # Mostra as espadas
zoro.executar_acao(navio)  # Ganha +30 de poder (3 espadas × 10)
```

---

### Classe `Navegador`

**Descrição:** Tripulante especializado em navegação e proteção do navio.

**Atributos Especiais:**
- `milhas_navegadas` (int): Total de milhas navegadas

**Método Especial:**
```python
# Incrementa milhas em 50 e marca rota como segura
# Protege o navio contra danos neste turno
navegador.executar_acao(navio)
```

**Exemplo:**
```python
from navegador import Navegador

nami = Navegador("Nami", recompensa=66.0, poder=40, milhas_navegadas=1000)
print(nami.milhas_navegadas)  # 1000
nami.executar_acao(navio)      # milhas → 1050, navio.rota_segura = True
```

---

### Classe `Medico`

**Descrição:** Tripulante especializado em cura e recuperação de energia.

**Atributos Especiais:**
- `pacientes_curados` (int): Total de pacientes já curados

**Método Especial:**
```python
# Cura o primeiro tripulante com status != "Ok"
# Ou o tripulante com menor energia
# Recupera 40 pontos de energia
medico.executar_acao(navio)
```

**Exemplo:**
```python
from medico import Medico

chopper = Medico("Chopper", recompensa=0.1, poder=30, pacientes_curados=50)
chopper.executar_acao(navio)   # Cura alguém, pacientes_curados → 51
```

---

### Classe `Cozinheiro`

**Descrição:** Tripulante especializado em preparação de refeições.

**Atributos Especiais:**
- `refeicoes_preparadas` (int): Total de refeições preparadas

**Método Especial:**
```python
# Aumenta energia de TODOS os tripulantes em 20 pontos
# Incrementa o contador de refeições
cozinheiro.executar_acao(navio)
```

**Exemplo:**
```python
from cozinheiro import Cozinheiro

sanji = Cozinheiro("Sanji", recompensa=330.0, poder=85, 
                   refeicoes_preparadas=500)
# Antes: todos com energia 50
sanji.executar_acao(navio)
# Depois: todos com energia 70 (+20 cada)
```

---

### Classe `Navio`

**Descrição:** Gerencia a tripulação e os atributos do navio.

**Atributos:**
- `nome` (str): Nome do navio
- `tripulacao` (list): Lista de Tripulante
- `vida` (int): Saúde do navio (0-100)
- `ouro` (int): Ouro acumulado (≥ 0)

**Métodos de Gestão:**
```python
# Recruta um novo tripulante (evita duplicatas)
navio.recrutar(tripulante)  # → bool

# Remove um tripulante pelo nome
navio.expulsar(nome)        # → bool

# Calcula poder total de todos os tripulantes
navio.calcular_poder_total()  # → int

# Obtém soma das recompensas
navio.recompensa_total      # → float

# Altera a vida do navio
navio.danificar(30)         # Vida -= 30
navio.reparar(20)           # Vida += 20

# Adiciona ouro
navio.ganhar_ouro(500)      # Ouro += 500

# Visualiza todos os tripulantes ordenados
navio.mostrar_manifesto()   # Imprime tabela formatada
```

**Exemplo:**
```python
from navio import Navio
from tripulante import Tripulante

navio = Navio("Going Merry")
luffy = Tripulante("Luffy", 1500.0, 95)
navio.recrutar(luffy)
navio.mostrar_manifesto()  # Mostra dados formatados
navio.danificar(25)        # Vida: 75
navio.salvar()             # Guarda em save.json
```

---

### Módulo `Persistencia`

**Descrição:** Gerencia salvar e carregar dados do navio em JSON.

**Funções:**
```python
# Salva o estado completo do navio (tripulação + atributos)
salvar_navio(navio_obj)

# Carrega um navio guardado pelo nome
# Se nome_navio é None, carrega o primeiro encontrado
carregar_navio(nome_navio=None)  # → Navio
```

**Formato JSON (save.json):**
```json
{
    "Going Merry": {
        "nome_navio": "Going Merry",
        "vida": 100,
        "ouro": 500,
        "tripulacao": [
            {
                "tipo": "Espadachim",
                "nome": "Zoro",
                "recompensa": 320.0,
                "poder": 90,
                "energia": 80,
                "status": "Ok",
                "espadas": ["Wado", "Enma"]
            }
        ]
    }
}
```

---

## Como Executar

### Requisitos
```bash
Python 3.10+
pip install colorama pytest
```

### Parte 1 - Menu Interativo
```bash
python tp1_p1_main.py
```

**Menu:**
```
--- One Piece: Grand Line Adventures ---
1 - Criar Navio
2 - Recrutar Tripulante
3 - Expulsar Tripulante
4 - Mostrar Manifesto
5 - Colocar Tripulante a Trabalhar
6 - Colocar Tripulante a Descansar
7 - Salvar Navio
8 - Carregar Navio
9 - Sair
```

### Parte 2 - Simulação Completa
```bash
python tp1_p2_main.py
```

Simulação com 10 turnos, eventos aleatórios e sistema de pontuação.

### Testes Unitários
```bash
pytest test_tp1_check.py -v
```

---

## Conceitos de POO Implementados

### 1. **Encapsulamento**
```python
# Uso de atributos privados (__) com properties
class Tripulante:
    def __init__(self, nome):
        self.__nome = nome  # Privado
    
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, valor):
        self.__nome = str(valor)
```

### 2. **Herança**
```python
# Espadachim herda de Tripulante
class Espadachim(Tripulante):
    def __init__(self, nome, espadas=None):
        super().__init__(nome)
        self.espadas = espadas or []
```

### 3. **Polimorfismo**
```python
# Cada subclasse implementa executar_acao() diferentemente
tripulante.executar_acao(navio)     # Mensagem genérica
espadachim.executar_acao(navio)     # Ataque com espadas
navegador.executar_acao(navio)      # Navegação
medico.executar_acao(navio)         # Cura
cozinheiro.executar_acao(navio)     # Refeição
```

### 4. **Métodos Mágicos**
```python
# __init__: Inicialização
# __str__: Representação em string
# __lt__: Comparação (<)
tripulantes_ordenados = sorted(tripulacao, reverse=True)
```

### 5. **Abstração**
- `executar_acao()` é abstrato na classe base
- Cada subclasse oferece implementação específica
- O cliente não precisa conhecer os detalhes

---

## Exemplo Completo de Uso

```python
from navio import Navio
from espadachim import Espadachim
from navegador import Navegador
from medico import Medico
from cozinheiro import Cozinheiro

# Criar navio
navio = Navio("Going Merry 2.0")

# Recrutar tripulação
zoro = Espadachim("Zoro", recompensa=320.0, poder=90, 
                  espadas=["Wado", "Enma"])
nami = Navegador("Nami", recompensa=66.0, poder=40, 
                 milhas_navegadas=1000)
chopper = Medico("Chopper", recompensa=0.1, poder=30)
sanji = Cozinheiro("Sanji", recompensa=330.0, poder=85)

for tripulante in [zoro, nami, chopper, sanji]:
    navio.recrutar(tripulante)

# Visualizar
navio.mostrar_manifesto()

# Executar ações
zoro.trabalhar(5)
sanji.executar_acao(navio)  # Todos recuperam energia
chopper.executar_acao(navio)  # Cura alguém

# Salvar
navio.salvar()

# Carregamento posterior
navio_carregado = Navio.carregar("Going Merry 2.0")
```

**Saída Esperada:**
```
==============================
MANIFESTO DO NAVIO: Going Merry 2.0
==============================
Nome: Zoro         | Função: Espadachim | Status: Ok | Poder:  90 | Recompensa: 320M | Energia: [#####.....] 50% | Espadas: Wado, Enma
Nome: Sanji        | Função: Cozinheiro | Status: Ok | Poder:  85 | Recompensa: 330M | Energia: [##########] 100% | Refeições: 1
Nome: Nami         | Função: Navegador  | Status: Ok | Poder:  40 | Recompensa: 66M  | Energia: [##########] 100% | Milhas: 1050
Nome: Chopper      | Função: Medico     | Status: Ok | Poder:  30 | Recompensa: 0M   | Energia: [##########] 100% | Curados: 1
==============================
Vida do Navio: 100%
Ouro: 0
Poder Total: 245
Recompensa Total: 716M
```

---

## Testes Unitários

O projeto inclui testes completos em `test_tp1_check.py`:

```bash
# Executar todos os testes
pytest test_tp1_check.py -v

# Executar tests de uma classe específica
pytest test_tp1_check.py::TestEspadachim -v

# Executar com cobertura
pytest test_tp1_check.py --cov
```

**Testes Incluidos:**
- Criação de tripulantes
- Propriedades e validações
- Métodos trabalhar/descansar
- Herança correta
- Polimorfismo executar_acao()
- Persistência salvar/carregar
- Manifesto do navio

---

## Eventos da Simulação (Parte 2)

| Evento | Tipo Ideal | Dano Vida | Dano Energia | Recompensa |
|--------|-----------|----------|-------------|-----------|
| 🦑 Kraken | Espadachim | 30 | 10 | 500 |
| 🌪️ Tempestade | Navegador | 40 | 5 | 100 |
| ⚓ Marinha | Espadachim | 20 | 20 | 300 |
| 🍒 Escorbuto | Cozinheiro | 0 | 30 | 0 |
| 🦠 Vírus | Medico | 0 | 40 | 0 |
| 🗺️ Tesouro | Navegador | 0 | 0 | 1000 |
| 🧜 Sereias | Medico | 25 | 10 | 200 |

---

## Tratamento de Erros

### Validações Automáticas

```python
# Energia sempre entre 0-100
tripulante.energia = 150  # → 100
tripulante.energia = -50  # → 0

# Poder sempre entre 0-100
tripulante.poder = 120   # → 100
tripulante.poder = -10   # → 0

# Recompensa sempre >= 0
tripulante.recompensa = -50  # → 0.0

# Vida do navio sempre entre 0-100
navio.vida = 150  # → 100
navio.vida = -30  # → 0

# Ouro sempre >= 0
navio.ouro = -500  # → 0
```

### Tratamento de Exceções

```python
try:
    tripulante = Tripulante("João", recompensa="invalido")
except ValueError:
    print("Recompensa deve ser um número")
```

---

## Notas Importantes

1. **JSON Automático**: O ficheiro `save.json` é criado automaticamente na primeira vez que se guarda um navio.

2. **Comparação de Tripulantes**: Usa sobrecarga de operador `<` baseada em poder e recompensa.

3. **Ordenação**: `sorted(tripulacao, reverse=True)` ordena do mais poderoso para o menos poderoso.

4. **Status Automático**: Um tripulante fica "Morto" quando sua energia chega a 0 após trabalho intenso.

5. **Polimorfismo em Ação**: Em `Simulacao._resolver_evento()`, o mesmo método `executar_acao()` funciona diferentemente para cada tipo de tripulante.

---

## Licença

Projeto criado para fins educacionais no contexto de Programação Orientada a Objetos.

---

## Personagens Exemplo (One Piece)

| Nome | Classe | Poder | Recompensa | Espadas/Atributo |
|------|--------|-------|-----------|------------------|
| Zoro | Espadachim | 90 | 320M | Wado, Enma, Shusui |
| Nami | Navegador | 40 | 66M | 1000 milhas |
| Chopper | Medico | 30 | 0.1M | 50 curados |
| Sanji | Cozinheiro | 85 | 330M | 500 refeições |
| Luffy | Tripulante | 95 | 1500M | - |

---
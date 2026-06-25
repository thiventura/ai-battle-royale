# AI Battle Arena

Uma arena de batalha em 2D onde personagens controlados por Inteligência Artificial competem até que apenas um sobreviva.

A ideia central é que cada participante crie seu próprio personagem e programa uma inteligência artificial para controlar suas ações dentro de uma arena. A qualidade da estratégia implementada determina quem sobreviverá.

O AI Battle Arena é um projeto desenvolvido em Python com o objetivo de unir programação, algoritmos e Inteligência Artificial em uma atividade prática e divertida. O projeto pode ser utilizado desde as primeiras disciplinas de programação, ajudando estudantes a praticarem conceitos fundamentais, ao mesmo tempo que também pode ser utilizado em disciplinas mais avançadas, permitindo explorar temas como agentes inteligentes, estratégias de busca e aprendizado de máquina.


## Conceito do jogo

O jogo é uma batalha no estilo Battle Royale, onde vários personagens controlados por IA lutam entre si. Cada personagem possui sua própria inteligência artificial, definida pelo participante, e deve tomar decisões a cada turno. A partida termina quando apenas um personagem permanece vivo.

A arena é um tabuleiro 2D com N colunas x M linhas (facilmente modificado). No início da partida, cada personagem recebe uma posição aleatória dentro do mapa. Os personagens não são controlados diretamente por jogadores. Cada um possui um arquivo de IA responsável por decidir suas ações.

Cada personagem possui:

**Vida (HP)**: Representa a quantidade de dano que o personagem consegue suportar. Quando a vida chega a 0 o personagem é eliminado da partida.

**Energia (EN)**: A energia é utilizada para executar ações especiais. A cada segundo, personagens vivos recuperam `+1` energia. A energia disponível limita a força dos ataques e defesas.

## Turnos do jogo

O jogo funciona em ciclos:

1. O jogo envia o estado atual para cada IA.
2. Cada personagem escolhe uma ação.
3. Os movimentos são realizados.
4. Defesas são aplicadas.
5. Ataques são executados.
6. Vida e energia são atualizadas.
7. Personagens derrotados são removidos.
8. Um novo turno começa.

O processo continua até existir apenas um personagem vivo.

## Ações disponíveis

Cada IA pode retornar uma das seguintes ações:

**Movimento**: O personagem pode andar em quatro direções (cima, baixo, esquerda, direita).

Exemplo:

```python
{
    "type": "move",
    "direction": "up"
}
```

**Ataque**: O personagem escolhe uma direção e quanto de energia deseja gastar. O ataque atinge somente a célula adjacente.

Exemplo:

```python
{
    "type": "attack",
    "direction": "right",
    "energy": 5
}
```

O dano é calculado:

```
Dano = Energia do ataque - Energia da defesa
```

Se o resultado for positivo, o valor é descontado da vida do alvo.

**Defesa**: O personagem pode gastar energia para reduzir danos recebidos.

Exemplo:

```python
{
    "type": "defend",
    "energy": 3
}
```

Quanto maior a energia usada, maior será a proteção.


## Criando um personagem

Cada participante deve criar uma pasta dentro de `characters/`. Exemplo:

```
characters/
└── Guerreiro/
    ├── ai.py
    └── sprite.png
```

O nome da pasta será o nome do personagem mostrado no jogo.


## Criando a inteligência artificial

O arquivo `ai.py` deve possuir uma função:

```python
def decide_action(state):
    ...
```

Essa função recebe o estado atual do jogo e retorna a ação escolhida.

Exemplo:

```python
def decide_action(state):

    return {
        "type": "move",
        "direction": "up"
    }
```

A IA recebe informações como:

* posição do personagem;
* vida atual;
* energia disponível;
* personagens próximos;
* todos os personagens da arena;
* personagens eliminados;
* quantidade de jogadores vivos.

Exemplo:

```python
{
    "turn": 10,

    "self": {
        "name": "Guerreiro",
        "x": 5,
        "y": 8,
        "life": 80,
        "energy": 6
    },

    "nearby": {
        "up": None,
        "down": {
            "name": "Mago",
            "life": 40,
            "energy": 5
        },
        "left": None,
        "right": None
    }
}
```

## Sprite do personagem

Cada personagem pode possuir uma imagem `sprite.png`. Essa imagem representa visualmente o personagem no jogo. Recomendações:

* formato PNG;
* imagem quadrada;
* imagem pequena;
* fundo transparente opcional.

O jogo redimensiona automaticamente para `32x32` pixels. Caso o arquivo não exista, um sprite padrão será criado automaticamente.


## Personagens de exemplo

O projeto já acompanha alguns personagens de exemplo implementados na pasta `characters/`. Esses personagens servem como referência para quem está começando e demonstram diferentes formas de criar estratégias para uma inteligência artificial. 

Cada personagem possui sua própria implementação do arquivo `ai.py` e pode ser utilizado como base para criar novas estratégias.


## Tecnologias utilizadas

* Python
* Pygame

Instalação:

```bash
pip install pygame
```

Execução:

```bash
python main.py
```


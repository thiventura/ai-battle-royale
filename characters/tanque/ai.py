import random

def decide_action(state):

    # Obtém as variáveis do estado atual necessárias
    energia = state["self"]["energy"]
    vida = state["self"]["life"]
    inimigo_up = state["nearby"]["up"]
    inimigo_down = state["nearby"]["down"]
    inimigo_left = state["nearby"]["left"]
    inimigo_right = state["nearby"]["right"]

    # Verifica se existe inimigo adjacente
    direcaoInimigo = None
    if inimigo_up is not None:
        direcaoInimigo = "up"
    elif inimigo_down is not None:
        direcaoInimigo = "down"
    elif inimigo_left is not None:
        direcaoInimigo = "left"
    elif inimigo_right is not None:
        direcaoInimigo = "right"

    # Se tiver bastante energia e inimigo próximo, faz um contra-ataque forte
    if energia >= 10 and direcaoInimigo is not None:
        return {
            "type": "attack",
            "direction": direcaoInimigo,
            "energy": energia
        }

    # Se tiver inimigo próximo, mas pouca energia, se protege
    if direcaoInimigo is not None:
        return {
            "type": "defend",
            "energy": 3
        }

    # Sem inimigos: anda aleatoriamente
    return {
        "type": "move",
        "direction": random.choice(["up","down","left","right"])
    }
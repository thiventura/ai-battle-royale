import random

def decide_action(state):

    # Obtém as variáveis do estado atual necessárias
    vida = state["self"]["life"]
    energia = state["self"]["energy"]
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

    # Se a vida estiver baixa, foge
    if vida < 40 and direcaoInimigo is not None:
        # Achando a direção oposta
        oposto = None
        if direcaoInimigo == "up":
            oposto = "down"
        elif direcaoInimigo == "left":
            oposto = "right"
        elif direcaoInimigo == "right":
            oposto = "left"
        else: 
            oposto = "up"

        return {
            "type": "move",
            "direction": oposto
        }

    # Se estiver com vida alta, ataque
    if direcaoInimigo is not None:
        return {
            "type": "attack",
            "direction": direcaoInimigo,
            "energy": 5
        }

    # Se não houver perigo, ande aleatoriamente
    return {
        "type": "move",
        "direction": random.choice(["up","down","left","right"])
    }
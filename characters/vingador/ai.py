import random

def decide_action(state):

    # Obtém as variáveis do estado atual necessárias
    nome = state["self"]["name"]
    vida = state["self"]["life"]
    energia = state["self"]["energy"]
    x = state["self"]["x"]
    y = state["self"]["y"]
    inimigo_up = state["nearby"]["up"]
    inimigo_down = state["nearby"]["down"]
    inimigo_left = state["nearby"]["left"]
    inimigo_right = state["nearby"]["right"]

    # Encontra o personagem com mais vida
    lider = None
    for character in state["characters"]:
        if not character["alive"]:
            continue

        if character["name"] == nome:
            continue

        if lider is None:
            lider = character
        elif character["life"] > lider["life"]:
            lider = character
    
    # Sem inimigos mais forte que eu
    if lider is None:
        return {
            "type": "defend",
            "energy": 0
        }


    # Verifica se existe inimigo adjacente e se ele é o lider
    direcaoInimigo = None
    if inimigo_up is not None and inimigo_up["name"] == lider["name"]:
        return {
            "type": "attack",
            "direction": "up",
            "energy": energia
        }
    elif inimigo_down is not None and inimigo_down["name"] == lider["name"]:
        return {
            "type": "attack",
            "direction": "down",
            "energy": energia
        }
    elif inimigo_left is not None and inimigo_left["name"] == lider["name"]:
        return {
            "type": "attack",
            "direction": "left",
            "energy": energia
        }
    elif inimigo_right is not None and inimigo_right["name"] == lider["name"]:
        return {
            "type": "attack",
            "direction": "right",
            "energy": energia
        }

    # Se não tem o líder perto, ande em direção do líder
    target_x = lider["x"]
    target_y = lider["y"]

    if target_x > x:
        return {
            "type": "move",
            "direction": "right"
        }

    if target_x < x:
        return {
            "type": "move",
            "direction": "left"
        }

    if target_y > y:
        return {
            "type": "move",
            "direction": "down"
        }

    if target_y < y:
        return {
            "type": "move",
            "direction": "up"
        }

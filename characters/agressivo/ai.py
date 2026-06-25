import random

def decide_action(state):

    # Obtém as variáveis do estado atual necessárias
    inimigo_up = state["nearby"]["up"]
    inimigo_down = state["nearby"]["down"]
    inimigo_left = state["nearby"]["left"]
    inimigo_right = state["nearby"]["right"]
    energia = state["self"]["energy"]

    # Ataca qualquer inimigo adjacente com toda a energia disponível
    if inimigo_up is not None:
        return {
                "type": "attack",
                "direction": "up",
                "energy": energia
            }

    if inimigo_down is not None:
        return {
                "type": "attack",
                "direction": "down",
                "energy": energia
            }

    if inimigo_left is not None:
        return {
                "type": "attack",
                "direction": "left",
                "energy": energia
            }

    if inimigo_right is not None:
        return {
                "type": "attack",
                "direction": "right",
                "energy": energia
            }

    # Se não houver inimigos próximos, movimenta-se aleatoriamente
    return {
        "type": "move",
        "direction": random.choice(["up", "down", "left", "right"])
    }
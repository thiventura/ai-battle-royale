def decide_action(state):

    # "state" armazena todas as informações de como está o jogo nesse momento
    # É possível extrair várias variáveis a partir dela

    # dados do jogo
    turn = state["turn"]                        # turno atual
    alive_count = state["alive_count"]          # quantos jogadores estão vivos
    characters = state["characters"]            # todos os jogadores

    # dados do próprio jogador
    me = state["self"]
    x = me["x"]                                 # posição X do jogador
    y = me["y"]                                 # posição Y do jogador
    life = me["life"]                           # vida (se chegar a zero, você perde)
    energy = me["energy"]                       # energia (usa tanto para atacar quanto para defender)

    # dados dos inimigos vizinhos
    inimigo_up = state["nearby"]["up"]          # inimigo que está acima. None se não tiver alguém perto
    inimigo_down = state["nearby"]["down"]      # inimigo que está abaixo. None se não tiver alguém perto
    inimigo_left = state["nearby"]["left"]      # inimigo que está à esquerda. None se não tiver alguém perto
    inimigo_right = state["nearby"]["right"]    # inimigo que está à direita. None se não tiver alguém perto

    # Exemplo de acessar dados de um inimigo que está logo acima de você
    if inimigo_up is not None:
        # se não for None, ou seja, se houver um inimigo acima
        inimigo_name = inimigo_up["name"]       # nome do inimigo
        inimigo_life = inimigo_up["life"]       # vida do inimigo
        inimigo_energy = inimigo_up["energy"]   # energia do inimigo

    
    # Agora que pode ter acesso a todas as variáveis, falta a decisão do que fazer neste turno
    # Toda a lógica para decidir a ação do personagem deve ser implementada aqui


    # Após decidir o que fazer, retorno a ação no formato correto
    # As ações possíveis são: mover, atacar e defender
    # A ação de movimento só requer a direção.
    # A ação de ataque, além da direção deve ser informado a energia do ataque
    # A ação de defesa, só requer a energia.
    return {
        "type": "attack",                   # "move", "attack" ou "defend"
        "direction": "right",               # "up", "down", "left" ou "right"
        "energy": 3                         # valor da força do ataque ou da defesa
    }

import sys
import pygame
from engine.game import Game
from engine.loader import CharacterLoader
from engine.renderer import Renderer, SCREEN_WIDTH, SCREEN_HEIGHT

FPS = 60
TURN_INTERVAL = 0.50
ENERGY_INTERVAL = 1.00

def create_game():
    loader = CharacterLoader()
    game = Game()
    characters = loader.load_characters()

    if len(characters) < 2:
        raise RuntimeError("São necessários pelo menos 2 personagens.")

    for character in characters:
        game.add_character(character)

    game.randomize_positions()

    return game


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Algoritmos I Battle Arena")
    
    clock = pygame.time.Clock()
    renderer = Renderer(screen)
    game = create_game()

    turn_timer = 0.0
    energy_timer = 0.0
    waiting_restart = False
    running = True

    while running:
        delta = (clock.tick(FPS)/ 1000.0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif (waiting_restart and event.type == pygame.KEYDOWN):
                game.reset()
                turn_timer = 0.0
                energy_timer = 0.0
                waiting_restart = False

        if not waiting_restart:
            turn_timer += delta
            energy_timer += delta
            game.update_effects(delta)

            if (energy_timer >= ENERGY_INTERVAL):
                energy_timer -= ENERGY_INTERVAL
                game.regenerate_energy()

            if (turn_timer >= TURN_INTERVAL):
                turn_timer -= TURN_INTERVAL
                game.execute_turn()
                winner = game.get_winner()
                if winner is not None:
                    waiting_restart = True

        else:
            game.update_effects(delta)

        renderer.draw(game)
        winner = game.get_winner()
        if (waiting_restart and winner is not None):
            renderer.draw_winner_screen(winner)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
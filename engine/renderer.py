import pygame
from engine.game import BOARD_WIDTH, BOARD_HEIGHT

CELL_SIZE = 64
GAME_WIDTH = BOARD_WIDTH * CELL_SIZE
GAME_HEIGHT = BOARD_HEIGHT * CELL_SIZE
PANEL_WIDTH = 320
SCREEN_WIDTH = GAME_WIDTH + PANEL_WIDTH
SCREEN_HEIGHT = GAME_HEIGHT


class Renderer:

    def __init__(self, screen):
        self.screen = screen

        pygame.font.init()

        self.font = pygame.font.SysFont("consolas", 18)
        self.small_font = pygame.font.SysFont("consolas", 14)
        self.big_font = pygame.font.SysFont("consolas", 36, bold=True)


    def draw(self, game):
        self.screen.fill((25, 25, 25))
        self.draw_board()
        self.draw_characters(game)
        self.draw_attack_effects(game)
        self.draw_panel(game)

    
    def draw_board(self):
        board_rect = pygame.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT)
        pygame.draw.rect(self.screen, (40, 40, 40), board_rect)

        for x in range(BOARD_WIDTH + 1):
            pygame.draw.line(self.screen, (70, 70, 70), (x * CELL_SIZE, 0), (x * CELL_SIZE, GAME_HEIGHT))

        for y in range(BOARD_HEIGHT + 1):
            pygame.draw.line(self.screen, (70, 70, 70), (0, y * CELL_SIZE), (GAME_WIDTH, y * CELL_SIZE))

    
    def draw_characters(self, game):

        for character in game.get_alive():

            px = (character.x * CELL_SIZE)
            py = (character.y * CELL_SIZE)
            self.screen.blit(character.sprite, (px, py))

            hp_text = self.small_font.render(str(character.life), True, (255, 255, 255))
            self.screen.blit(hp_text, (px + 2, py + 2))


    def draw_attack_effects(self, game):

        for effect in game.attack_effects:

            cx = (effect["x"] * CELL_SIZE) + CELL_SIZE // 2
            cy = (effect["y"] * CELL_SIZE) + CELL_SIZE // 2
            direction = (effect["direction"])
            tx = cx
            ty = cy

            if direction == "up":
                ty -= CELL_SIZE
            elif direction == "down":
                ty += CELL_SIZE
            elif direction == "left":
                tx -= CELL_SIZE
            elif direction == "right":
                tx += CELL_SIZE

            pygame.draw.line(self.screen, (255, 50, 50), (cx, cy), (tx, ty), 3)
            self.draw_arrow_head(tx, ty, direction)

    def draw_arrow_head(self, x, y, direction):
        size = 6
        if direction == "up":
            points = [(x, y - size), (x - size, y + size), (x + size, y + size)]
        elif direction == "down":
            points = [(x, y + size), (x - size, y - size), (x + size, y - size)]
        elif direction == "left":
            points = [(x - size, y), (x + size, y - size), (x + size, y + size)]
        else:
            points = [(x + size, y), (x - size, y - size), (x - size, y + size)]

        pygame.draw.polygon(self.screen, (255, 50, 50), points)

    
    def draw_panel(self, game):
        panel_x = GAME_WIDTH

        pygame.draw.rect(self.screen, (32, 32, 32), (panel_x, 0, PANEL_WIDTH, SCREEN_HEIGHT))

        y = 10
        y = self.draw_title("VIVOS", panel_x + 10, y)

        for char in game.get_alive():
            y = self.draw_character_info(char, panel_x + 10, y)

        y += 20
        y = self.draw_title("MORTOS", panel_x + 10, y )

        if len(game.death_order) == 0:
            text = self.small_font.render("Nenhum", True, (200, 200, 200) )
            self.screen.blit( text, (panel_x + 10, y))
            y += 25

        else:
            for idx, name in enumerate(game.death_order, start=1):
                text = (self.small_font.render(f"{idx}. {name}", True, (220, 220, 220)))
                self.screen.blit(text, (panel_x + 10, y))
                y += 20

        y += 20
        turn_text = self.font.render(f"Turno: {game.turn}", True, (255, 255, 255))
        self.screen.blit(turn_text, (panel_x + 10, y))

    
    def draw_title(self, text, x, y):
        rendered = self.font.render(text, True, (255, 255, 0))
        self.screen.blit(rendered, (x, y))
        return y + 30


    def draw_character_info(self, character, x, y):
        
        name = self.small_font.render(character.name, True, (255, 255, 255))
        self.screen.blit(name, (x, y))

        hp = self.small_font.render(f"HP: {character.life}", True, (150, 255, 150) )
        self.screen.blit(hp, (x + 150, y))

        energy = self.small_font.render(f"EN: {character.energy}", True, (150, 200, 255))
        self.screen.blit(energy, (x + 220, y))

        y += 15
        return y


    def draw_winner_screen(self, winner):

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render("VENCEDOR", True, (255, 255, 0))
        winner_text = self.big_font.render(winner.name, True, (255, 255, 255))
        restart_text = self.font.render("Pressione qualquer tecla para reiniciar", True, (255, 255, 255))

        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))

        self.screen.blit(title, title_rect)
        self.screen.blit(winner_text, winner_rect)
        self.screen.blit(restart_text, restart_rect)
from dataclasses import dataclass, field
import random

BOARD_WIDTH = 15
BOARD_HEIGHT = 10
INITIAL_LIFE = 100
INITIAL_ENERGY = 10
MAX_ENERGY = 20
ENERGY_REGEN = 3

@dataclass
class Character:

    name: str
    ai_module: object
    sprite: object

    x: int = 0
    y: int = 0

    life: int = INITIAL_LIFE
    energy: int = INITIAL_ENERGY

    alive: bool = True

    action: dict = field(default_factory=dict)

    defense_energy: int = 0


class Game:

    def __init__(self):
        self.characters = []
        self.turn = 0
        self.death_order = []
        self.attack_effects = []

    
    def add_character(self, character):
        self.characters.append(character)

    def get_alive(self):
        return [c for c in self.characters if c.alive]

    def get_winner(self):
        alive = self.get_alive()
        if len(alive) == 1:
            return alive[0]
        return None

    def randomize_positions(self):
        occupied = set()
        for char in self.characters:
            while True:
                x = random.randint(0, BOARD_WIDTH - 1)
                y = random.randint(0, BOARD_HEIGHT - 1)
                if (x, y) not in occupied:
                    occupied.add((x, y))
                    char.x = x
                    char.y = y
                    break

    def get_nearby(self, character):
        directions = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }

        nearby = {}

        for direction, (dx, dy) in directions.items():

            tx = character.x + dx
            ty = character.y + dy

            found = None
            for other in self.get_alive():

                if other == character:
                    continue

                if other.x == tx and other.y == ty:
                    found = {
                        "name": other.name,
                        "life": other.life,
                        "energy": other.energy
                    }
                    break

            nearby[direction] = found

        return nearby

    def get_state(self, character):
        return {
            "turn": self.turn,
            "board_width": BOARD_WIDTH,
            "board_height": BOARD_HEIGHT,
            "alive_count": len(self.get_alive()),
            "self": {
                "name": character.name,
                "x": character.x,
                "y": character.y,
                "life": character.life,
                "energy": character.energy
            },
            "nearby": self.get_nearby(character),
            "characters": [
                {
                    "name": c.name,
                    "x": c.x,
                    "y": c.y,
                    "life": c.life,
                    "energy": c.energy,
                    "alive": c.alive
                }
                for c in self.characters
            ],
            "dead_order": self.death_order.copy()
        }


    def collect_actions(self):
        for char in self.get_alive():
            try:
                state = self.get_state(char)
                action = (char.ai_module.decide_action(state))
                if not isinstance(action, dict):
                    action = {}
                char.action = action

            except Exception as ex:
                print(f"Erro IA {char.name}: {ex}")
                char.action = {}

    
    def process_movements(self):
        occupied = {
            (c.x, c.y)
            for c in self.get_alive()
        }

        directions = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }

        for char in self.get_alive():
            action = char.action

            if action.get("type") != "move":
                continue

            direction = action.get("direction")

            if direction not in directions:
                continue

            dx, dy = directions[direction]

            nx = char.x + dx
            ny = char.y + dy

            if nx < 0:
                continue

            if ny < 0:
                continue

            if nx >= BOARD_WIDTH:
                continue

            if ny >= BOARD_HEIGHT:
                continue

            if (nx, ny) in occupied:
                continue

            occupied.remove((char.x, char.y))

            char.x = nx
            char.y = ny
            occupied.add((char.x, char.y))

    
    def process_defenses(self):
        for char in self.get_alive():
            char.defense_energy = 0
            action = char.action

            if action.get("type") != "defend":
                continue

            energy = int(action.get("energy", 0))
            energy = max(0, energy)
            energy = min(energy, char.energy)
            char.energy -= energy
            char.defense_energy = energy


    def process_attacks(self):
        directions = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }

        attacks = []

        for attacker in self.get_alive():
            action = attacker.action
            if action.get("type") != "attack":
                continue

            direction = action.get("direction")
            if direction not in directions:
                continue

            energy = int(action.get("energy", 0))
            energy = max(0, energy)
            energy = min(energy, attacker.energy)

            if energy <= 0:
                continue

            attacker.energy -= energy

            dx, dy = directions[direction]
            tx = attacker.x + dx
            ty = attacker.y + dy

            target = None
            for other in self.get_alive():
                if other == attacker:
                    continue

                if (other.x == tx and other.y == ty):
                    target = other
                    break

            self.attack_effects.append({
                "x": attacker.x,
                "y": attacker.y,
                "direction":
                    direction,
                "timer": 0.20
            })

            if target is None:
                continue

            attacks.append((attacker, target, energy))

        for attacker, target, energy in attacks:
            damage = max(0, energy - target.defense_energy)
            target.life -= damage

    
    def remove_dead(self):
        for char in self.get_alive():
            if char.life > 0:
                continue

            char.alive = False

            self.death_order.append(char.name)

    
    def regenerate_energy(self):
        for char in self.get_alive():
            char.energy = min(MAX_ENERGY, char.energy + ENERGY_REGEN)

    
    def update_effects(self, delta):
        remaining = []

        for effect in self.attack_effects:
            effect["timer"] -= delta
            if effect["timer"] > 0:
                remaining.append(effect)

        self.attack_effects = remaining

    
    def execute_turn(self):
        self.turn += 1
        self.collect_actions()
        self.process_movements()
        self.process_defenses()
        self.process_attacks()
        self.remove_dead()
        self.regenerate_energy()

    
    def reset(self):
        self.turn = 0
        self.death_order.clear()
        self.attack_effects.clear()

        for char in self.characters:
            char.life = INITIAL_LIFE
            char.energy = INITIAL_ENERGY
            char.alive = True
            char.action = {}
            char.defense_energy = 0

        self.randomize_positions()
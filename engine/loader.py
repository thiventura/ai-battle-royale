import os
import importlib.util
import hashlib
import pygame
from engine.game import Character


CELL_SIZE = 64


class CharacterLoader:

    def __init__(self, characters_path="characters"):
        self.characters_path = characters_path

    
    def load_characters(self):
        characters = []

        if not os.path.exists(self.characters_path):
            raise FileNotFoundError(f"Pasta não encontrada: {self.characters_path}")

        for folder_name in sorted(os.listdir(self.characters_path)):
            folder_path = os.path.join(self.characters_path, folder_name)

            if not os.path.isdir(folder_path):
                continue

            character = (self._load_character(folder_name, folder_path))
            if character is not None:
                characters.append(character)

        return characters

    
    def _load_character(self, name, folder_path):
        ai_module = self._load_ai(name,folder_path)

        if ai_module is None:
            print(f"[ERRO] {name}: ai.py não encontrado")
            return None

        sprite = self._load_sprite(name,folder_path)

        character = Character(name=name, ai_module=ai_module, sprite=sprite)
        print(f"[OK] Personagem carregado: '{name}'")

        return character


    def _load_ai(self, name, folder_path):
        ai_path = os.path.join(folder_path,"ai.py")

        if not os.path.exists(ai_path):
            return None

        try:
            module_name = (f"character_{name}")
            spec = (importlib.util.spec_from_file_location(module_name, ai_path))
            module = (importlib.util.module_from_spec(spec))
            spec.loader.exec_module(module)
            
            if not hasattr(module,"decide_action"):
                print(f"[ERRO] {name}: função decide_action() não encontrada")
                return None

            return module

        except Exception as ex:
            print(f"[ERRO] Falha ao carregar {name}: {ex}")
            return None

    
    def _load_sprite(self, name, folder_path):
        sprite_path = os.path.join(folder_path, "sprite.png")

        if os.path.exists(sprite_path):
            try:
                image = pygame.image.load(sprite_path).convert_alpha()
                image = (pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE)))
                return image

            except Exception as ex:
                print(f"[AVISO] Erro ao carregar sprite de {name}: {ex}")

        return self._create_default_sprite(name)


    def _create_default_sprite(self,name):
        surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        color = self._color_from_name(name)
        pygame.draw.rect(surface, color, (0, 0, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, CELL_SIZE, CELL_SIZE), 2)
        return surface

    
    def _color_from_name(self, name):
        digest = hashlib.md5(name.encode()).digest()
        r = 80 + digest[0] % 150
        g = 80 + digest[1] % 150
        b = 80 + digest[2] % 150
        return (r,g,b)
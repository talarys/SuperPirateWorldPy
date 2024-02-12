# import settings
import pygame
import sys
import os
from level import Level
from settings import WINDOW_SIZE, FRAME_RATE
from pytmx.util_pygame import load_pygame

levels_path = os.path.join("data", "levels")


def get_levels(directory):
    levels = {}
    for level in os.listdir(directory):
        name, _ = os.path.splitext(level)
        levels[name] = os.path.join(directory, level)
    return levels


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Super Pirate World")
        self.clock = pygame.time.Clock()
        self.tmx_maps = get_levels(levels_path)
        self.current_stage = Level(load_pygame(self.tmx_maps["omni"]))

    def run(self):
        while True:
            dt = self.clock.tick(FRAME_RATE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_stage.run(dt)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()

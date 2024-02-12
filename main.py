# import settings
import pygame
import sys
from level import Level
from settings import WINDOW_SIZE


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Super Pirate World")
        self.current_stage = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_stage.run()
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()

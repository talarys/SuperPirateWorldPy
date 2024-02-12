import pygame
from pygame.math import Vector2 as vector


class Player(pygame.sprite.Sprite):
    def __init__(self, obj, groups):
        super().__init__(groups)
        self.image = pygame.Surface((obj.width, obj.height))
        self.image.fill("red")
        self.rect = self.image.get_frect(topleft=(obj.x, obj.y))
        self.direction = vector()
        self.speed = 0.2

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        self.direction = input_vector and input_vector.normalize()

    def move(self, dt):
        self.rect.topleft += self.direction * self.speed * dt

    def update(self, dt):
        self.input()
        self.move(dt)

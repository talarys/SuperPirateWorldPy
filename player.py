import pygame
from pygame.math import Vector2 as vector


class Player(pygame.sprite.Sprite):
    def __init__(self, obj, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((obj.width, obj.height))
        self.image.fill("red")
        self.rect = self.image.get_frect(topleft=(obj.x, obj.y))
        self.old_rect = self.rect.copy()
        self.direction = vector()
        self.speed = 200
        self.gravity = 2000
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        self.direction.x = input_vector.x and input_vector.normalize().x

    #
    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.handle_collision("x")

        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.handle_collision("y")

    def handle_collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == "x":
                    if (
                        self.rect.left < sprite.rect.right and self.direction.x < 0
                    ):  # moving left
                        self.rect.left = sprite.rect.right
                    if (
                        self.rect.right > sprite.rect.left and self.direction.x > 0
                    ):  # moving right
                        self.rect.right = sprite.rect.left
                else:
                    if (
                        self.rect.top < sprite.rect.bottom and self.direction.y < 0
                    ):  # moving up
                        self.rect.top = sprite.rect.bottom
                    if (
                        self.rect.bottom > sprite.rect.top and self.direction.y > 0
                    ):  # moving down
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)

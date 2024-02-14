import pygame
from pygame.math import Vector2 as vector


class Player(pygame.sprite.Sprite):
    def __init__(self, obj, groups, collision_sprites):
        super().__init__(groups)
        # TODO Replace with sprite
        self.image = pygame.Surface((obj.width, obj.height))
        self.image.fill("red")
        self.rect = self.image.get_frect(topleft=(obj.x, obj.y))
        self.old_rect = self.rect.copy()

        # Movement
        self.direction = vector()
        self.speed = 200
        self.jump = False
        self.jump_height = 1000
        self.gravity = 2000

        # Collision flags and data
        self.collision_sprites = collision_sprites
        self.on_surface = {"floor": False, "left": False, "right": False}

    # Input handler
    def input(self):
        pressed_keys = pygame.key.get_pressed()
        input_vector = vector()
        if pressed_keys[pygame.K_RIGHT]:
            input_vector.x += 1
        if pressed_keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_UP]:
            self.jump = True
        # Normalize X
        self.direction.x = input_vector.x and input_vector.normalize().x

    # Movement handler
    def move(self, dt):
        # X Moves
        self.rect.x += self.direction.x * self.speed * dt
        # X Collision check
        self.handle_collision("x")

        # Gravity
        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        # Y Collision check
        self.handle_collision("y")

        # Jump handler
        if self.jump:
            if self.on_surface["floor"]:
                self.direction.y = -self.jump_height
            self.jump = False

    def check_contact(self):
        floor_rect = pygame.Rect((self.rect.bottomleft), (self.rect.width, 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        # Collisions
        self.on_surface["floor"] = (
            True if floor_rect.collidelist(collide_rects) >= 0 else False
        )

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
        self.check_contact()

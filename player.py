import pygame
from pygame.math import Vector2 as vector
from timer import Timer


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

        # Timer
        self.timers = {"wall_jump": Timer(200)}

    # Input handler
    def input(self):
        pressed_keys = pygame.key.get_pressed()
        input_vector = vector()

        if not self.timers["wall_jump"].active:
            if pressed_keys[pygame.K_RIGHT]:
                input_vector.x += 1
            if pressed_keys[pygame.K_LEFT]:
                input_vector.x -= 1
            # Normalize X
            self.direction.x = input_vector.x and input_vector.normalize().x

        if pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_UP]:
            self.jump = True

    # Movement handler
    def move(self, dt):
        # X Moves
        self.rect.x += self.direction.x * self.speed * dt
        # X Collision check
        self.handle_collision("x")

        if (
            not self.on_surface["floor"]
            and self.on_surface["left"]
            or self.on_surface["right"]
        ):
            # Wall hug
            self.direction.y = 0
            self.rect.y += self.gravity / 10 * dt
        else:
            # Gravity
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt

        # Y Collision check
        self.handle_collision("y")

        # Jump handler
        if self.jump:
            # Normal jump
            if self.on_surface["floor"]:
                self.direction.y = -self.jump_height
            # Wall jump
            elif self.on_surface["left"] or self.on_surface["right"]:
                self.timers["wall_jump"].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface["left"] else -1
            self.jump = False

    def check_contact(self):
        floor_rect = pygame.Rect((self.rect.bottomleft), (self.rect.width, 2))
        left_rect = pygame.Rect(
            (self.rect.topleft + vector(-2, self.rect.height / 4)),
            (2, self.rect.height / 2),
        )
        right_rect = pygame.Rect(
            (self.rect.topright + vector(0, self.rect.height / 4)),
            (2, self.rect.height / 2),
        )

        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        # Collisions check
        self.on_surface["floor"] = floor_rect.collidelist(collide_rects) >= 0
        self.on_surface["left"] = left_rect.collidelist(collide_rects) >= 0
        self.on_surface["right"] = right_rect.collidelist(collide_rects) >= 0

    def handle_collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == "x":
                    # moving left
                    if (
                        self.rect.left <= sprite.rect.right
                        and self.old_rect.left >= sprite.old_rect.right
                    ):
                        self.rect.left = sprite.rect.right
                    # moving right
                    if (
                        self.rect.right >= sprite.rect.left
                        and self.old_rect.right <= sprite.old_rect.left
                    ):
                        self.rect.right = sprite.rect.left
                else:
                    # moving up
                    if (
                        self.rect.top < sprite.rect.bottom
                        and self.old_rect.top >= sprite.old_rect.bottom
                    ):
                        self.rect.top = sprite.rect.bottom
                    # moving down
                    if (
                        self.rect.bottom > sprite.rect.top
                        and self.old_rect.top <= sprite.old_rect.bottom
                    ):
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.update_timers()
        self.input()
        self.move(dt)
        self.check_contact()

import pygame

class Bird:
    def __init__(self):
        self.frames = [pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha()), pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha()), pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())]
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(100, 512))
        self.movement = 0

    def flap(self):
        self.movement = 0
        self.movement -= 12

    def animate(self):
        self.index = (self.index + 1) % len(self.frames)
        self.image = self.frames[self.index]

    def rotate(self):
        return pygame.transform.rotozoom(self.image, -self.movement * 3, 1)

    def update(self, gravity):
        self.movement += gravity
        self.rect.centery += self.movement

    def draw(self, screen):
        screen.blit(self.rotate(), self.rect)

    def reset(self):
        self.rect.center = (100, 512)
        self.movement = 0
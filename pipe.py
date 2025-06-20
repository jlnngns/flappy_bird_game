import pygame
import random

class PipeManager:
    def __init__(self):
        self.pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png'))
        self.pipe_height = [400, 600, 800]
        self.pipes = []

    def spawn_pipe(self):
        height = random.choice(self.pipe_height)
        bottom = self.pipe_surface.get_rect(midtop=(700, height))
        top = self.pipe_surface.get_rect(midbottom=(700, height - 300))
        self.pipes.extend([bottom, top])

    def move_pipes(self):
        for pipe in self.pipes:
            pipe.centerx -= 5
        self.pipes = [pipe for pipe in self.pipes if pipe.right > -50]

    def draw_pipes(self, screen):
        for pipe in self.pipes:
            if pipe.bottom >= 1024:
                screen.blit(self.pipe_surface, pipe)
            else:
                flipped = pygame.transform.flip(self.pipe_surface, False, True)
                screen.blit(flipped, pipe)

    def check_collision(self, bird_rect):
        for pipe in self.pipes:
            if bird_rect.colliderect(pipe):
                return True
        if bird_rect.top <= -100 or bird_rect.bottom >= 900:
            return True
        return False

    def reset(self):
        self.pipes.clear()
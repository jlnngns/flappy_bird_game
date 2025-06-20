import pygame

class UIManager:
    def __init__(self, font):
        self.font = font
        self.game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
        self.game_over_rect = self.game_over_surface.get_rect(center=(288, 512))

    def draw_score(self, screen, score):
        score_surface = self.font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

    def draw_game_over(self, screen, score, high_score):
        self.draw_score(screen, score)
        high_score_surface = self.font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(self.game_over_surface, self.game_over_rect)

    def draw_menu(self, screen):
        screen.blit(self.game_over_surface, self.game_over_rect)
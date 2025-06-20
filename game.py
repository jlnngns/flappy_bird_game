import pygame, sys
from bird import Bird
from pipe import PipeManager
from ui import UIManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((576, 1024))

        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('04B_19.tft', 40)

        self.gravity = 0.25
        self.state = "MENU"    # MENU, PLAYING, GAME_OVER
        self.bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert())
        self.floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png').convert())
        self.floor_x = 0

        self.bird = Bird()
        self.pipe_manager = PipeManager()
        self.ui = UIManager()

        self.score = 0
        self.high_score = 0
        self.can_score = True

        self.setup_events()
        self.load_sounds()
        
    def setup_events(self):
        self.SPAWNPIPE = pygame.USEREVENT
        self.BIRDFLAP = pygame.USEREVENT + 1

        pygame.time.set_timer(self.SPAWNPIPE, 1200)

        pygame.time.set_timer(self.BIRDFLAP, 200)

    def load_sounds(self):
        self.flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
        self.hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
        self.point_sound = pygame.mixer.Sound('sound/sfx_point.wav')

    def reset_game(self):
        self.state = "PLAYING"
        self.pipe_manager.reset()
        self.bird.reset()
        self.score = 0
        self.can_score = True

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(120)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == "MENU":
                        self.reset_game()
                    elif self.state == "PLAYING":
                        self.bird.flap()
                        self.flap_sound.play()
                    elif self.state == "GAME_OVER":
                        self.state = "MENU"
            
            if event.type == self.SPAWNPIPE and self.state == "PLAYING":
                self.pipe_manager.spawn_pipe()

            if event.type == self.BIRDFLAP:
                self.bird.animate()

    def update(self):
        if self.state == "PLAYING":
            self.bird.update(self.gravity)
            self.pipe_manager.move_pipes()

            if self.pipe_manager.check_collision(self.bird.rect):
                self.hit_sound.play()
                self.state = "GAME_OVER"
                self.high_score = max(self.score, self.high_score)

            self.check_score()

        self.floor_x -= 1
        if self.floor_x <= -576:
            self.floor_x = 0

    def check_score(self):
        for pipe in self.pipe_manager.pipes:
            if 95 < pipe.centerx < 105 and self.can_score:
                self.score += 1
                self.point_sound.play()
                self.can_score = False
            if pipe.centerx < 0:
                self.can_score = True

    def draw(self):
        self.screen.blit(self.bg_surface, (0, 0))

        if self.state == "MENU":
            self.ui.draw_menu(self.screen)
        elif self.state == "PLAYING":
            self.pipe_manager.draw_pipes(self.screen)
            self.bird.draw(self.screen)
            self.ui.draw_score(self.screen, self.score)
        elif self.state == "GAME_OVER":
            self.pipe_manager.draw_pipes(self.screen)
            self.bird.draw(self.screen)
            self.ui.draw_game_over(self.screen, self.score, self.high_score)

        self.screen.blit(self.floor_surface, (self.floor_x, 900))

        self.screen.blit(self.floor_surface, (self.floor_x + 576, 900))
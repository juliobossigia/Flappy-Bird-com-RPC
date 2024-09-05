import pygame
import sys
import random
import rpyc
from rpyc.utils.server import OneShotServer
from threading import Thread

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (34, 24))
pipe_image = pygame.image.load("pipe.png")
pipe_image = pygame.transform.scale(pipe_image, (52, 320))

GRAVITY = 0.25
BIRD_JUMP = -6
PIPE_SPEED = 3
PIPE_GAP = 150
SPEED_INCREMENT = 0.3 

def draw_bird(bird):
    screen.blit(bird_image, (bird['x'], bird['y']))

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_image, (pipe['x'], pipe['y']))
        screen.blit(pygame.transform.flip(pipe_image, False, True), (pipe['x'], pipe['y'] - pipe_image.get_height() - PIPE_GAP))
        
def generate_pipes():
    y = random.randint(200, 400)
    return [{'x': SCREEN_WIDTH, 'y': y}, {'x': SCREEN_WIDTH, 'y': y - PIPE_GAP - pipe_image.get_height()}]

def check_collision(bird, pipes):
    bird_rect = pygame.Rect(bird['x'], bird['y'], bird_image.get_width(), bird_image.get_height())
    for pipe in pipes:
        pipe_rect = pygame.Rect(pipe['x'], pipe['y'], pipe_image.get_width(), pipe_image.get_height())
        if bird_rect.colliderect(pipe_rect):
            return True
    if bird['y'] <= 0 or bird['y'] >= SCREEN_HEIGHT:
        return True
    return False

class FlappyBirdService(rpyc.Service):
    client_connected = False
    record_score = 0

    def on_connect(self, conn):
        if FlappyBirdService.client_connected:
            print("Já possui um cliente conectado. Tente mais tarde")
            
        else:
            FlappyBirdService.client_connected = True
            print("Cliente conectado com sucesso!")

    def on_disconnect(self, conn):
        FlappyBirdService.client_connected = False
        print("Cliente desconectado!")

    def __init__(self):
        self.game_running = False
        self.bird = {'x': 50, 'y': 300, 'vel_y': 0}
        self.pipes = generate_pipes()
        self.score = 0

    def exposed_get_score(self):
        return self.score

    def exposed_get_record(self):
        return FlappyBirdService.record_score

    def exposed_start_game(self):
        if not self.game_running:
            self.game_running = True
            self.bird = {'x': 50, 'y': 300, 'vel_y': 0}
            self.pipes = generate_pipes()
            self.score = 0  
            return "Game Started"
        return "Game já está sendo executando"

    def exposed_bird_jump(self):
        if self.game_running:
            self.bird['vel_y'] = BIRD_JUMP

    def exposed_is_game_over(self):
        return not self.game_running

    def run_game(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.game_running:
                self.bird['vel_y'] += GRAVITY
                self.bird['y'] += self.bird['vel_y']

                current_pipe_speed = PIPE_SPEED + self.score * SPEED_INCREMENT

                for pipe in self.pipes:
                    pipe['x'] -= current_pipe_speed
                if self.pipes[0]['x'] < -pipe_image.get_width():
                    self.pipes.pop(0)
                    self.pipes.pop(0)
                    self.pipes.extend(generate_pipes())
                    self.score += 1
                

                    if self.score > FlappyBirdService.record_score:
                        FlappyBirdService.record_score = self.score

                    print(self.score)

                if check_collision(self.bird, self.pipes):
                    self.game_running = False  # Fim do jogo

            screen.fill((135, 206, 235))
            draw_bird(self.bird)
            draw_pipes(self.pipes)
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    service = FlappyBirdService()
    server = OneShotServer(service, hostname="172.30.30.18", port=9090)

    game_thread = Thread(target=service.run_game)
    game_thread.daemon = True #se o programa principal terminar todas as threads terminam
    game_thread.start()

    print("Starting Flappy Bird Server...")
    server.start()

import rpyc
import pygame
import sys

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Client")

font = pygame.font.SysFont(None, 55)
Press_Space = font.render('Press Space', True, (255, 255, 255))
background_color = (0, 128, 128)

def main():
    try:
        conn = rpyc.connect("172.30.30.18", 9090)
        flappy_bird_service = conn.root

        clock = pygame.time.Clock()
        game_started = False 
        game_over = False
        connection_message = ""

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not game_started and not game_over:
                            connection_message = flappy_bird_service.start_game()
                            if connection_message == "Game Started":
                                game_started = True
                                game_over = False
                            
                        elif game_started:
                            flappy_bird_service.bird_jump()

                    if event.key == pygame.K_s and game_over:
                        connection_message = flappy_bird_service.start_game()
                        if connection_message == "Game Started":
                            game_started = True
                            game_over = False

            screen.fill(background_color)
            if game_started:
                score = flappy_bird_service.get_score() 
                record_score = flappy_bird_service.get_record()
                score_text = font.render(f"Score: {score}", True, (255, 255, 255))
                record_text = font.render(f"Record: {record_score}", True, (255, 255, 0))
                screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))  
                screen.blit(record_text, (SCREEN_WIDTH // 2 - record_text.get_width() // 2, 100))  

                # Verifica se o jogo terminou
                if flappy_bird_service.is_game_over():
                    game_started = False
                    game_over = True

            if game_over:
                game_over_text = font.render("Game Over", True, (255, 0, 0))
                restart_text = font.render("Press 'S' to Restart", True, (255, 255, 255))
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
                screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 300))
            
            else:
                screen.blit(Press_Space, (SCREEN_WIDTH // 2 - Press_Space.get_width() // 2, SCREEN_HEIGHT // 2 - Press_Space.get_height() // 2))

            pygame.display.update()
            clock.tick(60)

    except ConnectionRefusedError:
        print("Não foi possível conectar ao servidor. Verifique se o servidor está em execução e tente novamente.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()

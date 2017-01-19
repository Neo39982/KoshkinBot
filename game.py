import pygame
import animation

def game_start():
    pygame.init()
    screen = pygame.display.set_mode((1920, 480))
    pygame.display.set_caption("Python/Pygame Animation")
    clock = pygame.time.Clock()
    player = animation.Serge((32, 32))

    game_over = False

    while game_over == False:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        player.handle_event(event)
        screen.fill(pygame.Color("white"))
        screen.blit(player.image, player.rect)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
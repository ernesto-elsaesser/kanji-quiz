import pygame


pygame.init()

screen = pygame.display.set_mode((640, 480))
font = pygame.font.SysFont("dejavusansmono", 48)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if event.key == 104:
                running = False

            screen.fill((0, 0, 0))
            text_surface = font.render(str(event.key), True, (255, 255, 255))
            rect = text_surface.get_rect(center=(320, 240))
            screen.blit(text_surface, rect)
            pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()

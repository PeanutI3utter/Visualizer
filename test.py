import pygame

pygame.init()
window = pygame.display.set_mode((800, 600))
window.fill((255, 255, 255))
surface1 = pygame.Surface((600, 400))
surface1.fill((0,0,0))
surface2 = pygame.Surface((700, 500))
surface2.fill((0, 0, 0))

surface1.blit(surface2, (50, 50))   
window.blit(surface1, (50, 50))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
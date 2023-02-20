import pygame

n = int(input())
width1 = 40
height1 = 300
x = 136.5
y = 0
if __name__ == '__main__':
    pygame.init()
    size = width, height = 300, 300
    screen = pygame.display.set_mode(size)
    pygame.draw.ellipse(screen, (255, 255, 255), (0, 0, 300, 300), 1)
    pygame.display.flip()
    for i in range(1, n):
        pygame.draw.ellipse(screen, (255, 255, 255), (x, y, width1, height1), 1)
        pygame.draw.ellipse(screen, (255, 255, 255), (y, x, height1, width1), 1)
        pygame.display.flip()
        width1 += 28
        x -= 15
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
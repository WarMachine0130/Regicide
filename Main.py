import sys, pygame
pygame.init()
import Card

size = width, height = 800, 600
speed = [2, 2]
black = 0, 0, 0
poolFeltGreen = 39, 119, 20

screen = pygame.display.set_mode((size), pygame.RESIZABLE)
pygame.display.set_caption('Test')

ball = pygame.image.load("assets\Playing Cards\card-spades-1.png")
ballrect = ball.get_rect()
#ballrect.center = width//2, height//2

moving = False

while True:
    pygame.draw.rect(screen, "white", ballrect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ballrect.collidepoint(event.pos):
                moving = True
        elif event.type == pygame.MOUSEBUTTONUP:
            moving = False
        elif event.type == pygame.MOUSEMOTION and moving:
            ballrect.move_ip(event.rel)

            #ballrect = ballrect.move(speed)
    #if ballrect.left < 0 or ballrect.right > width:
        #speed[0] = -speed[0]
    #if ballrect.top < 0 or ballrect.bottom > height:
        #speed[1] = -speed[1]

    screen.fill(poolFeltGreen)
    screen.blit(ball, ballrect)
    pygame.display.flip()
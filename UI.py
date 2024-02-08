import pygame
import subprocess

pygame.init()

screen = pygame.display.set_mode((722, 563))

pygame.display.set_caption("MLYNEK")

#images
boardImg = pygame.image.load('static/ui.jpeg')
coords = {
	0: (35, 400, 38, 403),
	1: (35, 463, 38, 466),
}
# clickables = [pygame.Rect(500, 500, 35, 35) ]

mul = 1
clickables = [pygame.Rect(mul*c[0], mul*c[1], 170, 30) for c in coords.values()]
screen.blit(boardImg, (0, 0))

pygame.display.flip()\
# print(clickables)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                for i,area in enumerate(clickables):
                    if area.collidepoint(event.pos):
                        if i == 0:
                            subprocess.Popen(["python", "main.py"])
                            pygame.quit()  # Close the current window
                            running = False
                            break
                        if i == 1:
                            subprocess.Popen(["python", "main4.py"])
                            pygame.quit()  # Close the current window
                            running = False
                            break
                        
                        # print(clickables[i])

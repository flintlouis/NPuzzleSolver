import pygame
import sys

GRIDSIZE = 100

FPS = 100

GRAY = (100,100,100)
BLACK = (0,0,0)
WHITE = (255,255,255)

UP = (-1, 0)
DOWN = (1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)

def handleKeys(settings):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE and not settings.running:
				if settings.reset:
					settings.running = True
				elif not settings.reset:
					settings.reset = True
			elif event.key == ord('r'):
				settings.shuffle = True

import pygame
from info import *
import os
from draw import drawPuzzle, drawNumbers, draw, drawPath
from settings import Settings
import numpy as np
from npuzzle import NPuzzle

def initPygame(screenWidth, screenHeight):
	# Initiate Pygame
	pygame.init()
	pygame.display.set_caption("Name")
	screen = pygame.display.set_mode((screenWidth, screenHeight), 0, 32)
	surface = pygame.Surface(screen.get_size())
	surface = surface.convert()
	return surface, screen


def main(n):
	os.system("clear")
	print("Loading...")
	# Init NPuzzle
	N = NPuzzle((n,n))
	# Init settings
	settings = Settings(N.puzzle.shape)
	settings.clock = pygame.time.Clock()
	surface, screen = initPygame(settings.screenWidth, settings.screenHeight)
	settings.myfont = pygame.font.SysFont("arialbold", 60)
	settings.shuffle = True
	os.system("clear")
	# Start mainloop
	while True:
		handleKeys(settings)
		if settings.running and settings.reset:
			N.reset()
			print("Solving puzzle...")
			solution = N.solve_puzzle(settings)
			os.system("clear")
			if solution:
				print(f"Solved in {solution.g} steps")
				drawPath(solution, screen, surface, settings)
			settings.running = False
			settings.reset = False
		if not settings.running and settings.reset:
			os.system("clear")
			draw(screen, surface, settings, N)
		if settings.shuffle:
			N.puzzle = N.end
			N.shuffle(50)
			settings.shuffle = False
			settings.reset = True

if len(sys.argv) != 2:
	exit("\nUsage: python main.py <number between 2-5>\n")
n = sys.argv[1]
if not n.isnumeric() or int(n) < 2 or int(n) > 5:
	exit("\nUsage: python main.py <number between 2-5>\n")

main(int(n))

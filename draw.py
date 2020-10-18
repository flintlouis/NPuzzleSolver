import pygame
import numpy as np
from info import *

def drawRect(surface, point, colour):
	i, j = point
	r = pygame.Rect(j, i, GRIDSIZE, GRIDSIZE)
	pygame.draw.rect(surface, colour, r) 
	pygame.draw.rect(surface, BLACK, r, 1)

def drawPuzzle(surface, settings, empty):
	for j in range(settings.gridWidth):
		for i in range(settings.gridHeight):
			if not empty[i][j]:
				drawRect(surface, (i*GRIDSIZE, j*GRIDSIZE), WHITE)
			else:
				drawRect(surface, (i*GRIDSIZE, j*GRIDSIZE), GRAY)

def draw(screen, surface, settings, N):
	drawPuzzle(surface, settings, (N.puzzle == 0))
	screen.blit(surface, (0,0))
	drawNumbers(screen, N.puzzle, settings.myfont, settings)
	pygame.display.update()

def drawNumbers(screen, puzzle, myfont, settings):
	for j in range(settings.gridWidth):
		for i in range(settings.gridHeight):
			n = puzzle[i][j]
			if not n:
				continue
			offset = 0
			if n < 10:
				offset = 15
			text = myfont.render(f" {n}", 1, BLACK)
			screen.blit(text, ((j*GRIDSIZE)+offset, (i*GRIDSIZE)+15))

def timesPoints(pointA, n):
	return (pointA[0]*n, pointA[1]*n)

def sumPoints(pointA, pointB):
	return (pointA[0]+pointB[0], pointA[1]+pointB[1])

def	minusPoints(pointA, pointB):
	return (pointA[0]-pointB[0], pointA[1]-pointB[1])

def getRowCol(index, shape):
	row, col = shape
	return int(index / row), (index % col)

def getEmpty(puzzle):
	for i in range(puzzle.size):
		if not np.concatenate(puzzle)[i]:
			return getRowCol(i, puzzle.shape)

def getDir(a, b):
	for i in range(a.size):
		if not np.concatenate(a)[i]:
			break
	for j in range(b.size):
		if not np.concatenate(b)[j]:
			break
	pointA = getRowCol(i, a.shape)
	pointB = getRowCol(j, a.shape)
	return minusPoints(pointB, pointA)

def drawPath(path, screen, surface, settings):
	# Draw puzzle states recursively
	if not path.prev:
		return
	drawPath(path.prev, screen, surface, settings)
	dir = getDir(path.puzzle, path.prev.puzzle)
	drawMove(screen, surface, path.prev.puzzle, getEmpty(path.puzzle), dir, settings)

def	drawMove(screen, surface, puzzle, point, dir, settings):
	# Animate move
	i, j = point
	start  = (i*GRIDSIZE, j*GRIDSIZE)
	end = sumPoints(point, dir)
	end = (end[0]*GRIDSIZE, end[1]*GRIDSIZE)
	current = start

	while current != end:
		settings.clock.tick(100)
		handleKeys(settings)
		drawRect(surface, start, GRAY)
		drawRect(surface, end, GRAY)

		current = sumPoints(current, timesPoints(dir, 5))
		drawRect(surface, current, WHITE)
		screen.blit(surface, (0,0))

		for j in range(settings.gridWidth):
			for i in range(settings.gridHeight):
				n = puzzle[i][j]
				if not n:
					continue
				offset = 0
				if n < 10:
					offset = 15
				text = settings.myfont.render(f" {n}", 1, BLACK)
				if (i,j) == point:
					screen.blit(text, ((current[1])+offset, (current[0])+15))
				else:
					screen.blit(text, ((j*GRIDSIZE)+offset, (i*GRIDSIZE)+15))

		pygame.display.update()

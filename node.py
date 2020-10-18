import numpy as np
from npuzzle import NPuzzle

class Node(NPuzzle):

	# Total cost
	f = 0
	# Cost taken to current state of puzzle
	g = 0
	# Distance of current state to solved state
	h = 0

	def __init__(self, puzzle, end=None, g=0, prev=None):
		super().__init__(puzzle.shape, puzzle)
		if not (end is None):
			self.end = end
		else:
			self.end = self.fill_spiral()
		self.g = g
		self.calc_h()
		self.calc_f()
		self.prev = prev

	def calc_f(self):
		self.f = self.g + self.h
	
	def calc_h(self):
		# Calculate distance from current state to solved state using Manhatten distance
		puzzle = self.puzzle.reshape(-1)
		end = self.end.reshape(-1)
		h = 0
		for i in range(self.puzzle.size):
			for j in range(self.puzzle.size):
				if puzzle[i] and puzzle[i] == end[j]:
					p = np.unravel_index(i, self.size)
					e = np.unravel_index(j, self.size)
					sub = np.subtract(p,e)
					h += abs(sub[0]) + abs(sub[1])
					break
		self.h = h

	def update(self, g, prev):
		self.g = g
		self.calc_f()
		self.prev = prev

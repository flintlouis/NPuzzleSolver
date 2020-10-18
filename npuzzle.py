import numpy as np
from info import handleKeys

class NPuzzle():
	# List of nodes that are still available to visit
	openset = []
	# List of nodes that are already visited
	closedset = []

	def __init__(self, size, puzzle=None):
		self.size = size
		self.x, self.y = size
		if not (puzzle is None):
			self.puzzle = puzzle
		else:
			self.init_puzzle()
		self.end = self.fill_spiral()

	def reset(self):
		self.openset = []
		self.closedset = []

	def init_puzzle(self):
		self.puzzle = np.zeros(self.size, dtype=int)
		self.puzzle = self.fill_spiral()

	def fill_spiral(self):
		# Returns Npuzzle in solved spiral form
		value = 1
		h, w = 0, 0
		x, y = self.x, self.y
		puzzle = np.copy(self.puzzle)
		while h < x and w < y:
			value = self.fill_right(h,w,y,puzzle,value)
			h += 1
			y -= 1
			value = self.fill_down(h,x,y,puzzle,value)
			if h < x:
				x -= 1
				value = self.fill_left(w,x,y,puzzle,value)
			if w < y:
				value = self.fill_up(h,w,x,puzzle,value)
				w += 1
		puzzle[np.unravel_index(puzzle.argmax(),puzzle.shape)] = 0
		return puzzle

	def fill_right(self, h, start, end, puzzle, value):
		for i in range(start, end):
			puzzle[h][i] = value
			value += 1
		return value

	def fill_down(self, start, end, y, puzzle, value):
		for i in range(start, end):
			puzzle[i][y] = value
			value += 1
		return value

	def fill_left(self, end, x, start, puzzle, value):
		for i in range(start - 1, end - 1, -1):
			puzzle[x][i] = value
			value += 1
		return value

	def fill_up(self, end, w, start, puzzle, value):
		for i in range(start - 1, end - 1, -1):
			puzzle[i][w] = value
			value += 1
		return value

	def move_up(self, verbose=False):
		# Move empty space up
		new = np.copy(self.puzzle)
		empty = np.unravel_index(new.argmin(),new.shape)
		i, j = empty[0] - 1, empty[1]
		if i < 0:
			return new
		new[empty], new[i][j] = new[i][j], 0
		return new

	def move_down(self, verbose=False):
		# Move empty space down
		new = np.copy(self.puzzle)
		empty = np.unravel_index(new.argmin(),new.shape)
		i, j = empty[0] + 1, empty[1]
		if i >= self.x:
			return new
		new[empty], new[i][j] = new[i][j], 0
		return new	

	def move_left(self, verbose=False):
		# Move empty space left
		new = np.copy(self.puzzle)
		empty = np.unravel_index(new.argmin(),new.shape)
		i, j = empty[0], empty[1] - 1
		if j < 0:
			return new
		new[empty], new[i][j] = new[i][j], 0
		return new

	def move_right(self, verbose=False):
		# Move empty space right
		new = np.copy(self.puzzle)
		empty = np.unravel_index(new.argmin(),new.shape)
		i, j = empty[0], empty[1] + 1
		if j >= self.y:
			return new
		new[empty], new[i][j] = new[i][j], 0
		return new

	def shuffle(self, n, verbose=False):
		# Shuffle puzzle n random moves, set verbose to true to print the moves
		f = [self.move_up, self.move_down, self.move_left, self.move_right]
		for i in range(n):
			np.random.shuffle(f)
			self.puzzle = f[0](verbose)

	def check_set(self, Set, puzzle):
		# Check if puzzlestate is in Set
		for node in Set:
			if (node.puzzle == puzzle).all():
				return node
		return False

	def solve_puzzle(self, settings):
		from node import Node
		# Put current node in openset
		self.openset.append(Node(np.copy(self.puzzle), self.end))
		# While openset is not empty
		while self.openset:
			handleKeys(settings)
			# Find node with the lowest f in openset
			current = self.openset[0]
			for node in self.openset:
				if node.f < current.f:
					current = node
			# Remove node from openset and add to closedset
			self.closedset.append(self.openset.pop(self.openset.index(current)).puzzle)
			# If current.puzzle is in solved state stop the while loop
			if (current.puzzle == self.end).all():
				return current
			# Array with all moves available from current node, aka neighboring nodes
			neighbors = [current.move_up(),
					current.move_down(),
					current.move_left(),
					current.move_right()]
			# Checks if neigbor is valid and add them to openset if necessary
			for neighbor in neighbors:
				# If neigbor in closedset continue
				if np.any(np.all(self.closedset == neighbor, axis=(1, 2))):
					continue
				g = current.g + 1
				# Check if neigbor is in openset, and if so if it has a lower g then the current one
				node = self.check_set(self.openset, neighbor)
				if node:
					if g < node.g:
						node.update(g, current)
				# Add to openset
				else:
					node = Node(neighbor, self.end, g, current)
					self.openset.append(node)

		return False

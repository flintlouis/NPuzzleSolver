from info import GRIDSIZE

class Settings():

	myfont = None
	running = False
	clock = None
	reset = True
	shuffle = False

	def __init__(self, size):
		self.screenWidth = size[1]*GRIDSIZE
		self.screenHeight = size[0]*GRIDSIZE
		self.gridWidth = int(self.screenWidth / GRIDSIZE)
		self.gridHeight = int(self.screenHeight / GRIDSIZE)
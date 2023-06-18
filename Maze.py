import pygame as pg
from pygame.locals import RESIZABLE
import random
pg.init()
pg.display.set_caption('An Epic Maze')
# random.seed(349823416782364589023453456458)

# Constants:
width = 90
height = 50
startpos = (45, 25)
cellLength = 20
wallWidth = 3

# Colors:
white = (255,255,255)
black = (0,0,0)
grey = (128,128,128)
dark_grey = (50,50,50)

red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)


# Calculated Constants
displayW = width * cellLength
displayH = height * cellLength
clock = pg.time.Clock()
screen = pg.display.set_mode((displayW, displayH))
tickrate = 60

unvisitedColor = black
visitedColor = (25,43,100)
finishedColor = grey
currentColor = red
wallColor = white

class Board:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.make_cells()
		self.make_borders()

	def make_cells(self):
		cells = []
		for j in range(height):
			cells.append([])
			for i in range(width):
				cells[-1].append(Cell(self, (i, j)))
		self.cells = cells

	def make_borders(self):
		for j, row in enumerate(self.cells):
			for i, cell in enumerate(row):
				if j == 0:
					cell.walls[1] = True
				if j == len(self.cells) - 1:
					cell.walls[3] = True
				if i == 0:
					cell.walls[0] = True
				if i == len(row) - 1:
					cell.walls[2] = True


	def draw_cells(self):
		for row in self.cells:
			for cell in row:
				color = cell.determine_color()
				cell.draw(color)

	def draw_walls(self):
		for row in self.cells:
			for cell in row:
				cell.draw_walls()

class Cell:

	walls_key = {
	0: ((0, 1), (0, 0)), 
	1: ((0, 0), (1, 0)), 
	2: ((1, 0), (1, 1)), 
	3: ((1, 1), (0, 1))
	}

	adjacent_cells_key = {
	0: (-1, 0), 
	1: (0, -1), 
	2: (1,  0), 
	3: (0,  1)
	}

	def __init__(self, board, pos):
		self.board = board
		self.pos = pos
		self.i = pos[0]
		self.j = pos[1]
		self.walls = [0, 0, 0, 0]
		self.visited = False
		self.finished = False

	def draw(self, color):
		x = self.i * cellLength
		y = self.j * cellLength
		pg.draw.rect(screen, color, (x, y, cellLength, cellLength))

	def determine_color(self):
		#Error handling if entity has not been created yet
		try:
			if self == entity.currentCell:
				return currentColor
		except NameError:
			pass
		if self.finished:	
			return finishedColor
		elif self.visited:
			return visitedColor
		else:
			return unvisitedColor

	def draw_walls(self):
		for b, wall in enumerate(self.walls):
			if wall:
				relposes = Cell.walls_key[b]
				x1 = (self.i + relposes[0][0]) * cellLength
				y1 = (self.j + relposes[0][1]) * cellLength

				x2 = (self.i + relposes[1][0]) * cellLength 
				y2 = (self.j + relposes[1][1]) * cellLength

				pg.draw.line(screen, wallColor, (x1, y1), (x2, y2), wallWidth)

	def surrounding_cells(self):
		"""NOTE: WILL RETURN A LIST WITH 1 or more "None" in it if the cell is on the border"""
		cells = []
		for b in range(4):
			relpos = Cell.adjacent_cells_key[b]
			new_i = self.i + relpos[0]
			new_j = self.j + relpos[1]
			if not (new_i < 0 or new_i >= self.board.width or new_j < 0 or new_j >= self.board.height):
				cells.append(self.board.cells[new_j][new_i])
			else:
				cells.append(None)
		return cells

	def __repr__(self):
		return str(self.pos)

class Entity:

	inverse_direction_key = {0:2, 1:3, 2:0, 3:1}

	def __init__(self, board, pos=(0,0)):
		self.board = board
		self.pos = pos
		self.i = pos[0]
		self.j = pos[1]
		self.currentCell = board.cells[self.j][self.i]
		self.currentCell.visited = True
		self.done = False

	def step(self):
		surroundingCells = self.currentCell.surrounding_cells()
		unvisitedCells = []
		for direction, cell in enumerate(surroundingCells):
			if cell != None:
				if not cell.visited:
					unvisitedCells.append((cell, direction))

		if len(unvisitedCells) == 0:
			for direction, cell in enumerate(surroundingCells):
				if cell != None:
					if not self.currentCell.walls[direction] and not cell.finished:
						nextCell = cell
						break
			else:
				nextCell = self.currentCell

			self.currentCell.finished = True

		else:
			nextPair = random.choice(unvisitedCells)
			nextCell = nextPair[0]
			direction = nextPair[1]

			nextCell.visited = True
			nextSurroundingCells = nextCell.surrounding_cells()
			for direction, cell in enumerate(nextSurroundingCells):
				if cell != None:
					if cell.visited and not cell == self.currentCell:
						nextCell.walls[direction] = True
						cell.walls[Entity.inverse_direction_key[direction]] = True

		if self.currentCell == nextCell:
			self.done = True
		self.currentCell = nextCell

def main(running=False):
	global tickrate
	global board
	global entity
	board = Board(width, height)
	board.make_borders()

	entity = Entity(board, startpos)

	locked = True
	while locked:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				locked = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					locked = False
				elif event.key == pg.K_SPACE:
					running = not running
				elif event.key == pg.K_RETURN:
					entity.step()
				elif event.key == pg.K_r:
					main(running)
				elif event.key == pg.K_LEFT:
					if tickrate > 5:
						tickrate -= 5
				elif event.key == pg.K_RIGHT:
					tickrate += 5
				elif event.key == pg.K_c:
					pass
		if running:
			entity.step()
		screen.fill(black)
		board.draw_cells()
		board.draw_walls()
		pg.display.update()
		if entity.done:
			board.cells[0][0].walls[0] = False
			board.cells[height - 1][width - 1].walls[2] = False
		clock.tick(tickrate)
	pg.quit()

main()
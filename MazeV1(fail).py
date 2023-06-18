import pygame as pg
from pygame.locals import RESIZABLE
import random
pg.init()
pg.display.set_caption('An Epic Maze')
random.seed(349823416782364589023453456458)

# Constants:
width = 10
height = 10
startpos = (0,0)
cellLength = 30
wallWidth = 5

# Colors:
white = (255,255,255)
black = (0,0,0)
grey = (128,128,128)
dark_grey = (50,50,50)

red = (255,0,0)
blue = (0,0,255)


# Calculated Constants
displayW = width * cellLength
displayH = height * cellLength
clock = pg.time.Clock()
screen = pg.display.set_mode((displayW, displayH))

unvisitedColor = white
visitedColor = blue
finishedColor = grey
class Wall:
	def __init__(self, active=False):
		self.active = active

	def __bool__(self):
		return self.active

	def draw(self, cell, isVertical, color=dark_grey):
		if color == None:
			color = dark_grey
		if self.active:
			color = black
		if isVertical:
			x1 = (cell.i + 1) * cellLength
			x2 = x1
			y1 = (cell.j) * cellLength
			y2 = (cell.j + 1) * cellLength

		else:
			x1 = (cell.i) * cellLength
			x2 = (cell.i + 1) * cellLength
			y1 = (cell.j + 1) * cellLength
			y2 = y1

		pos1 = (x1, y1)
		pos2 = (x2, y2)
		print(color)
		pg.draw.line(screen, color, pos1, pos2, wallWidth)

class Cell:

	def __init__(self, i, j):
		self.i = i
		self.j = j
		self.coords = (i,j)
		self.walls = [None, None, None, None]
		self.needsUpdate = True
		self.visited = False
		self.finished = False

	def draw(self):
		if self.visited:
			if self.finished:
				color = finishedColor
			else:
				color = visitedColor
		else:
			color = unvisitedColor

		x = self.i * cellLength
		y = self.j * cellLength
		pg.draw.rect(screen, color, (x,y, cellLength, cellLength))

	def draw_walls(self, color=None):
		"""Draws all the walls around self"""
		try:
			self.walls[0].draw(self, True, color)
		except AttributeError:
			pass
		try:
			self.walls[1].draw(self, False, color)
		except AttributeError:
			pass
		try:
			self.walls[2].draw(self, True, color)
		except AttributeError:
			pass
		try:	
			self.walls[3].draw(self, False, color)
		except AttributeError:
			pass

class Board:

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.cells = []
		self.make_cells()
		self.walls = []
		self.make_walls()
		self.finished = False

	def make_cells(self):
		"""Makes all cells and assigns them to self.walls"""
		for j in range(height):
			self.cells.append([])
			for i in range(width):
				self.cells[j].append(Cell(i,j))

	def make_walls(self):
		"""Makes all walls, assigns them to cells and assigns them to self.cells
		[0] = Left
		[1] = Top
		[2] = Right
		[3] = Bottom
		"""
		for row in self.cells:
			for cell in row:
				if cell.j == 0:
					upper = Wall()
					cell.walls[1] = upper
					self.walls.append(upper)

				if cell.i == 0:
					left = Wall()
					cell.walls[0] = left
					self.walls.append(left)

				vertical = Wall()
				cell.walls[2] = vertical
				if cell.i != width - 1:
					self.cells[cell.j][cell.i + 1].walls[0] = vertical
					self.walls.append(vertical)

				horizontal = Wall()
				cell.walls[3] = vertical
				if cell.j != height - 1:
					self.cells[cell.j + 1][cell.i].walls[1] = vertical
					self.walls.append(horizontal)

	def update(self):
		"""Draws the entire board (cells and walls) and checks for finished condition"""
		unfinished = []
		for row in self.cells:
			for cell in row:
				if not cell.finished:
					unfinished.append(cell)
				if cell.needsUpdate:
					cell.draw()
		for row in self.cells:
			for cell in row:
				cell.draw_walls()
				cell.needsUpdate = False
		if len(unfinished) == 0:
			self.finished = True



class Entity:

	def __init__(self, board, pos=(0,0)):
		self.pos = pos
		self.board = board
		self.cell = board.cells[pos[1]][pos[0]]
		self.key = {0:(-1, 0), 1:(0, 1), 2:(1,0), 3:(0,-1)}
		self.cell.visited = True

	def move(self, new_cell):
		previousCell = self.cell
		self.cell = new_cell

		if previousCell.visited and self.cell.visited:
			previousCell.finished = True
		else:
			self.cell.visited = True

		adjacentCells = self.get_adjacent_cells()
		for b, cell in enumerate(adjacentCells):
			if cell.visited and cell != previousCell:
				print('cell found')
				print(b)
				self.cell.walls[b].active = True
				print(self.cell.walls[b].active)
				print(self.cell.walls[b+2].active)
		previousCell.needsUpdate = True
		self.cell.needsUpdate = True

	def step(self):
		"""The main logic performed each step. Will decide which cell to move to.
		WARNING: THIS METHOD ASSUMES THERE IS A POSSIBLE CELL TO MOVE TO"""
		unvisited = []
		unfinished_and_accesible = None
		adjacentCells = self.get_adjacent_cells()
		for b, cell in enumerate(adjacentCells):
			accessible = not self.cell.walls[b]

			if not cell.visited:
				unvisited.append(cell)
			if not cell.finished and accessible:
				unfinished_and_accesible = cell
		if len(unvisited) != 0:
			new_cell = random.choice(unvisited)
		else:
			new_cell = unfinished_and_accesible

		self.move(new_cell)

	def get_adjacent_cells(self):
		"""returns a list of the cell objects that are orthogonally adjacent to self: [left, top, right, bottom]"""
		cells = []
		for direction in range(4):
			displacement = self.key[direction]
			try:
				cells.append(self.board.cells[self.cell.j + displacement[1]][self.cell.i + displacement[0]])
			except IndexError:
				pass
		return cells

def finished():
	print('maze done bro')
	while True:
		for event in pg.event.get():
			if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
				pg.quit()
				quit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_r:
					main()

def main():
	global board
	board = Board(width, height)
	board.make_cells()
	board.make_walls()
	board.cells[5][5].draw_walls(color=red)
	entity = Entity(board)
	screen.fill(white)

	board.update()
	pg.display.update()

	runautomatically = False
	locked = True
	while locked:
		if runautomatically:
			entity.step()
		for event in pg.event.get():
			if event.type == pg.QUIT:
				locked = False
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					locked = False
				elif event.key == pg.K_RETURN:
					entity.step()
					board.update()
					board.cells[5][5].draw_walls(color=red)
					
				elif event.key == pg.K_SPACE:
					runautomatically = not runautomatically

		pg.display.update()
		clock.tick(60)
		if board.finished:
			finished()

	pg.quit()

main()
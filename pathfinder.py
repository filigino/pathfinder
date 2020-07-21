import pygame
import math
from queue import PriorityQueue

WINDOW_WIDTH = 800
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))
pygame.display.set_caption("A* Pathfinder")

ROWS = 50 # also number of columns

RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
TURQUOISE = (64, 224, 208)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

BLANK = WHITE
START = ORANGE
END = BLUE
OPEN = GREEN
CLOSED = RED
BARRIER = BLACK
PATH = PURPLE

class Node:
	def __init__(self, col, row, width, total_rows):
		self.col = col
		self.row = row
		self.x = col * width
		self.y = row * width
		self.width = width
		self.total_rows = total_rows
		self.colour = BLANK
		self.neighbours = []

	def get_position(self):
		return self.col, self.row

	def is_start(self):
		return self.colour == START

	def is_end(self):
		return self.colour == END

	def is_open(self):
		return self.colour == OPEN

	def is_closed(self):
		return self.colour == CLOSED

	def is_barrier(self):
		return self.colour == BARRIER

	def is_path(self):
		return self.colour == PATH

	def reset(self):
		self.colour = BLANK

	def mark_start(self):
		self.colour = START

	def mark_end(self):
		self.colour = END

	def mark_open(self):
		self.colour = OPEN

	def mark_closed(self):
		self.colour = CLOSED

	def mark_barrier(self):
		self.colour = BARRIER

	def mark_path(self):
		self.colour = PATH

	def draw(self, window):
		pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.width))

	def update_neighbours(self, grid):
		pass

	# less than
	# comparator?
	def __lt__(self, other):
		return False

def make_grid(window_width, rows):
	grid = []
	node_width = window_width // rows # integer division

	cols = rows
	for i in range(cols):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, node_width, rows)
			grid[i].append(node)

	return grid

# Draw each node
def draw(window, window_width, rows, grid):
	window.fill(WHITE)

	for col in grid:
		for node in col:
			node.draw(window)

	draw_grid(window, window_width, rows)
	pygame.display.update()

def draw_grid(window, window_width, rows):
	node_width = window_width // rows

	cols = rows
	for i in range(cols):
		# Vertical line
		pygame.draw.line(window, GREY, (i * node_width, 0), (i * node_width, window_width))
		for j in range(rows):
			# Horizontal line
			pygame.draw.line(window, GREY, (0, j * node_width), (window_width, j * node_width))

def get_clicked_node(window_width, rows, grid):
	x, y = pygame.mouse.get_pos()
	node_width = window_width // rows

	col = x // node_width
	row = y // node_width

	node = grid[col][row]
	return node

# heuristic function using Manhattan distance
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def main(window, window_width, rows):
	grid = make_grid(window_width, rows)

	# Like null
	start = None
	end = None

	# Booleans are capitalized
	run = True
	started = False

	while run:
		# Draw each node
		draw(window, window_width, rows, grid)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if started:
				continue

			# left click
			if pygame.mouse.get_pressed()[0]:
				node = get_clicked_node(window_width, rows, grid)

				if not start and node != end:
					start = node
					start.mark_start()
				elif not end and node != start:
					end = node
					end.mark_end()
				elif node != start and node != end:
					node.mark_barrier()
			# right click
			elif pygame.mouse.get_pressed()[2]:
				node = get_clicked_node(window_width, rows, grid)
				node.reset()

				if node == start:
					start = None
				elif node == end:
					end = None
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and not started:
					for col in grid:
						for node in col:
							pass
							# node.update_neighbours(grid)

					# algorithm(lambda: draw(window, window_width, rows, grid), grid, start, end)
				elif event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(window_width, rows)


	pygame.quit()

main(WINDOW, WINDOW_WIDTH, ROWS)

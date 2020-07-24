import pygame
import math
from queue import Queue
import heapq

WINDOW_WIDTH = 864
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))
pygame.display.set_caption("Pathfinder")

ROWS = 50 # also number of columns

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
START = (255, 165, 0) # orange
END = (0, 0, 255) # blue
OPEN = (0, 255, 0) # green
VISITED = (128, 0, 128) # purple
BARRIER = (0, 0, 0) # black
PATH = (64, 224, 208) # turquoise

class Node:
	def __init__(self, col, row, width):
		self.col = col
		self.row = row
		self.width = width
		self.colour = WHITE

	def get_position(self):
		return self.col, self.row

	def is_visited(self):
		return self.colour == VISITED

	def is_barrier(self):
		return self.colour == BARRIER

	def reset(self):
		self.colour = WHITE

	def mark_start(self):
		self.colour = START

	def mark_end(self):
		self.colour = END

	def mark_open(self):
		self.colour = OPEN

	def mark_visited(self):
		self.colour = VISITED

	def mark_barrier(self):
		self.colour = BARRIER

	def mark_path(self):
		self.colour = PATH

	def draw(self, window):
		pygame.draw.rect(window, self.colour, (self.col * self.width, self.row * self.width, self.width, self.width))

def create_node_grid(window_width, rows):
	node_grid = []
	node_width = window_width // rows # integer division

	cols = rows
	for i in range(cols):
		node_grid.append([])
		for j in range(rows):
			node = Node(i, j, node_width)

			# border
			if i < 2 or i > (rows - 3) or j < 2 or j > (rows - 3):
				node.mark_barrier()

			node_grid[i].append(node)
	return node_grid

# Draw each node
def draw(window, window_width, rows, node_grid):
	for col in node_grid:
		for node in col:
			node.draw(window)

	draw_grid(window, window_width, rows)
	pygame.display.update()

def draw_grid(window, window_width, rows):
	node_width = window_width // rows

	for i in range(rows):
		# Vertical line
		pygame.draw.line(window, GREY, (i * node_width, 0), (i * node_width, window_width))
		# Horizontal line
		pygame.draw.line(window, GREY, (0, i * node_width), (window_width, i * node_width))

def get_clicked_node(window_width, rows, node_grid):
	x, y = pygame.mouse.get_pos()
	node_width = window_width // rows

	col = x // node_width
	row = y // node_width

	node = node_grid[col][row]
	return node

def find_path_DFS(node_grid, node, start, end, found, previous, draw):
	if node == end:
		draw_path(previous, start, end, draw)
		return True
	else:
		if node != start:
			node.mark_visited()

		neighbours_list = get_neighbours(node, node_grid)
		for neighbour in neighbours_list:
			if not neighbour.is_visited() and neighbour != start:
				neighbour.mark_open()
				previous[neighbour] = node
				draw()
				found = find_path_DFS(node_grid, neighbour, start, end, found, previous, draw)
				if found:
					return True


def find_path_BFS(node_grid, start, end, draw):
	queue = Queue()
	queue.put(start)
	marked = {start} # set
	previous = {} # dictionary

	while queue:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		node = queue.get()
		if node == end:
			draw_path(previous, start, end, draw)
			return
		else:
			if node != start:
				node.mark_visited()

			neighbours_list = get_neighbours(node, node_grid)
			for neighbour in neighbours_list:
				if neighbour not in marked:
					queue.put(neighbour)
					marked.add(neighbour)

					neighbour.mark_open()
					previous[neighbour] = node
			draw()

# f_score = g_score + h_score
def find_path_a_star(node_grid, start, end, draw):
	# priority queue returns min, compares next value if tie
	open_set = []

	# break ties with whichever node was examined first
	count = 0

	# (f_score, count, node)
	heapq.heappush(open_set, (0, count, start))

	# for checking if a node is in open set
	marked = {start}

	# list comprehension
	g_score = {node: float("inf") for col in node_grid for node in col}
	g_score[start] = 0

	f_score = {node: float("inf") for col in node_grid for node in col}
	f_score[start] = g_score[start] + h(start, end)

	# dictionary
	previous = {}

	while open_set:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		# 2 refers to node itself (f_score, count, node)
		node = heapq.heappop(open_set)[2]
		marked.remove(node)

		if node == end:
			draw_path(previous, start, end, draw)
			return
		else:
			neighbours_list = get_neighbours(node, node_grid)

			for neighbour in neighbours_list:
				temp_g_score = g_score[node] + 1

				if temp_g_score < g_score[neighbour]:
					g_score[neighbour] = temp_g_score
					f_score[neighbour] = temp_g_score + h(neighbour, end)
					previous[neighbour] = node
					if neighbour not in marked:
						count += 1
						heapq.heappush(open_set, (f_score[neighbour], count, neighbour))
						marked.add(neighbour)
						neighbour.mark_open()

			if node != start:
				node.mark_visited()

			draw()

def get_neighbours(node, node_grid):
	neighbours = []
	col, row = node.get_position()

	# up
	if (row - 1) >= 0 and not node_grid[col][row - 1].is_barrier():
		neighbours.append(node_grid[col][row - 1])
	# right
	if (col + 1) < len(node_grid) and not node_grid[col + 1][row].is_barrier():
		neighbours.append(node_grid[col + 1][row])	
	# down
	if (row + 1) < len(node_grid) and not node_grid[col][row + 1].is_barrier():
		neighbours.append(node_grid[col][row + 1])
	# left
	if (col - 1) >= 0 and not node_grid[col - 1][row].is_barrier():
		neighbours.append(node_grid[col - 1][row])

	return neighbours

def draw_path(previous, start, end, draw):
	end.mark_end()
	path = []
	node = previous[end]

	while node != start:
		path.append(node)
		node = previous[node]
	while path:
		path.pop().mark_path()
		draw()

def h(start, end):
	x1, y1 = start.get_position()
	x2, y2 = end.get_position()
	return abs(x1 - x2) + abs(y1 - y2)

def main(window, window_width, rows):
	rows += 4
	node_grid = create_node_grid(window_width, rows)

	# Like null
	start = None
	end = None

	# Booleans are capitalized
	run = True

	while run:
		# Draw each node
		draw(window, window_width, rows, node_grid)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			# left click
			if pygame.mouse.get_pressed()[0]:
				node = get_clicked_node(window_width, rows, node_grid)

				col, row = node.get_position()
				if col > 1 and col < (rows - 2) and row > 1 and row < (rows - 2):
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
				node = get_clicked_node(window_width, rows, node_grid)
				col, row = node.get_position()
				if col > 1 and col < (rows - 2) and row > 1 and row < (rows - 2):
					node.reset()

					if node == start:
						start = None
					elif node == end:
						end = None
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					start = None
					end = None
					node_grid = create_node_grid(window_width, rows)
				elif start and end:
					if event.key == pygame.K_d:
						found = False
						previous = {}
						
						# lambda function
						# anonymous functions are useful for defining functions that will only be used once
						# used here bc simpler than passing all arguments just to call draw() repeatedly
						find_path_DFS(node_grid, start, start, end, found, previous, lambda: draw(window, window_width, rows, node_grid))
					elif event.key == pygame.K_b:
						find_path_BFS(node_grid, start, end, lambda: draw(window, window_width, rows, node_grid))
					elif event.key == pygame.K_a:
						find_path_a_star(node_grid, start, end, lambda: draw(window, window_width, rows, node_grid))
	pygame.quit()

main(WINDOW, WINDOW_WIDTH, ROWS)

import sys
from collections import deque
from PIL import Image, ImageDraw

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class CustomStackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        else:
            node = self.frontier.pop()
            return node

class CustomQueueFrontier(CustomStackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        else:
            node = self.frontier.pop(0)
            return node

class MazeSolver:
    def __init__(self, maze_file):
        self.maze, self.start, self.goal = self.load_maze(maze_file)
        self.solution = None
        self.explored = set()
        self.num_explored = 0

    def load_maze(self, maze_file):
        with open(maze_file, 'r') as f:
            maze = [list(line.strip()) for line in f.readlines()]

        start, goal = None, None
        for i in range(len(maze)):
            for j in range(len(maze[i]):
                if maze[i][j] == 'A':
                    start = (i, j)
                elif maze[i][j] == 'B':
                    goal = (i, j)
        
        return maze, start, goal

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < len(self.maze) and 0 <= c < len(self.maze[0]) and self.maze[r][c] != '█':
                result.append((action, (r, c)))
        return result

    def solve(self):
        start_node = (self.start, [])
        frontier = CustomQueueFrontier()
        frontier.add(start_node)
        while frontier:
            current_state, path = frontier.remove()
            self.num_explored += 1
            if current_state == self.goal:
                self.solution = path
                break
            if current_state in self.explored:
                continue
            self.explored.add(current_state)
            for action, neighbor in self.neighbors(current_state):
                new_path = path + [action]
                frontier.add((neighbor, new_path))
    
    def output_image(self, output_file, show_solution=True, show_explored=False):
        cell_size = 50
        cell_border = 2

        img_width = len(self.maze[0]) * cell_size
        img_height = len(self.maze) * cell_size
        img = Image.new("RGBA", (img_width, img_height), "black")
        draw = ImageDraw.Draw(img)

        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                fill = (40, 40, 40) if self.maze[i][j] == '█' else (237, 240, 252)
                if (i, j) == self.start:
                    fill = (255, 0, 0)
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)
                elif show_solution and self.solution and (i, j) in self.solution:
                    fill = (220, 235, 113)
                elif show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(output_file)

if len(sys.argv) != 2:
    sys.exit("Usage: python maze_solver.py maze.txt")

solver = MazeSolver(sys.argv[1])
print("Maze:")
for row in solver.maze:
    print("".join(row))
print("Solving...")
solver.solve()
print("States Explored:", solver.num_explored)
print("Solution:")
for action in solver.solution:
    print(action)
solver.output_image("maze_solution.png", show_explored=True)

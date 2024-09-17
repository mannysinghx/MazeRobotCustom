# maze.py
import tkinter as tk
from tkinter import messagebox
import random
from collections import deque

class MazeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Maze Generator")
        
        self.canvas = None
        self.size_x = 10
        self.size_y = 10
        self.cell_size = 30
        self.start = None
        self.end = None
        self.walls = set()
        self.path = []
        self.robot = None  # To hold the robot's representation
        
        self.create_widgets()
        self.draw_maze()

    def create_widgets(self):
        self.size_x_entry = tk.Entry(self.master)
        self.size_x_entry.pack(side=tk.TOP, padx=5, pady=5)
        self.size_y_entry = tk.Entry(self.master)
        self.size_y_entry.pack(side=tk.TOP, padx=5, pady=5)
        
        self.create_button = tk.Button(self.master, text="Create Maze", command=self.create_maze)
        self.create_button.pack(side=tk.TOP, padx=5, pady=5)
        
        self.solve_button = tk.Button(self.master, text="Solve Maze", command=self.solve_maze)
        self.solve_button.pack(side=tk.TOP, padx=5, pady=5)

        # Color selection buttons
        self.color_selection_frame = tk.Frame(self.master)
        self.color_selection_frame.pack(side=tk.BOTTOM, padx=5, pady=5)

        self.selected_color = 'green'  # Default selected color

        def select_color(color):
            self.selected_color = color

        self.green_button = tk.Button(self.color_selection_frame, text="Green", bg='green', command=lambda: select_color('green'))
        self.green_button.pack(side=tk.LEFT, padx=5)

        self.red_button = tk.Button(self.color_selection_frame, text="Red", bg='red', command=lambda: select_color('red'))
        self.red_button.pack(side=tk.LEFT, padx=5)

        self.black_button = tk.Button(self.color_selection_frame, text="Black", bg='black', command=lambda: select_color('black'))
        self.black_button.pack(side=tk.LEFT, padx=5)

    def create_maze(self):
        self.size_x = int(self.size_x_entry.get())
        self.size_y = int(self.size_y_entry.get())
        self.walls.clear()
        self.start = None
        self.end = None
        self.draw_maze()

    def draw_maze(self):
        if self.canvas:
            self.canvas.destroy()
        self.canvas = tk.Canvas(self.master, width=self.size_x * self.cell_size, height=self.size_y * self.cell_size)
        self.canvas.pack()
        
        # Bind mouse click to place colors on the maze after the canvas is created
        self.canvas.bind("<Button-1>", self.place_color)
        
        for x in range(self.size_x):
            for y in range(self.size_y):
                color = 'white'  # Default color for empty cells
                if (x, y) in self.walls:
                    color = 'black'
                elif (x, y) == self.start:
                    color = 'green'
                elif (x, y) == self.end:
                    color = 'red'
                self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                              (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                              fill=color)

        # Draw the robot at the starting position
        if self.start:
            self.draw_robot()

    def draw_robot(self):
        if self.robot:
            self.canvas.delete(self.robot)  # Remove the old robot if it exists
        x, y = self.start
        self.robot = self.canvas.create_oval(x * self.cell_size + 5, y * self.cell_size + 5,
                                              (x + 1) * self.cell_size - 5, (y + 1) * self.cell_size - 5,
                                              fill='blue')  # Robot represented as a blue circle

    def place_color(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 0 <= x < self.size_x and 0 <= y < self.size_y:
            if self.selected_color == 'black':
                self.walls.add((x, y))
            elif self.selected_color == 'green':
                self.start = (x, y)  # Set start point
            elif self.selected_color == 'red':
                self.end = (x, y)  # Set end point
            self.draw_maze()  # Redraw the maze to show the new color

    def solve_maze(self):
        if not self.start or not self.end or self.start == self.end:
            messagebox.showwarning("Warning", "Please set start and end points.")
            return
        
        if not self.has_all_colors():
            messagebox.showwarning("Warning", "Please place all 3 colors (start, end, walls).")
            return
        
        self.path = self.bfs(self.start, self.end)
        
        # Check if the path is empty (unsolvable maze)
        if not self.path:
            messagebox.showwarning("Warning", "The maze is unsolvable.")
            return
        
        self.animate_solution()

    def has_all_colors(self):
        return self.start and self.end and len(self.walls) > 0

    def bfs(self, start, end):
        queue = deque([start])
        visited = {start}
        parent = {start: None}
        
        while queue:
            current = queue.popleft()
            if current == end:
                break
            
            # Visualize the current cell being explored with a small yellow dot
            x, y = current
            self.canvas.create_oval(x * self.cell_size + self.cell_size // 3, y * self.cell_size + self.cell_size // 3,
                                    (x + 1) * self.cell_size - self.cell_size // 3, (y + 1) * self.cell_size - self.cell_size // 3,
                                    fill='yellow')  # Smaller yellow dot to visualize exploration
            self.master.update()
            self.master.after(100)  # Delay to visualize the exploration
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if (0 <= neighbor[0] < self.size_x and
                    0 <= neighbor[1] < self.size_y and
                    neighbor not in visited and
                    neighbor not in self.walls):
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current
        
        path = []
        while end in parent:
            path.append(end)
            end = parent[end]
        return path[::-1]

    def animate_solution(self):
        for step in self.path:
            x, y = step
            # Paint the box green as the robot moves
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                          (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                          fill='green')  # Paint the path green
            self.master.update()
            self.master.after(100)  # Delay for visualization

        # Move the robot along the path
        self.move_robot()

    def move_robot(self):
        if not self.path:
            return
        
        for step in self.path:
            x, y = step
            self.canvas.move(self.robot, (x * self.cell_size + self.cell_size // 2) - (self.canvas.coords(self.robot)[0] + self.cell_size // 2),
                                          (y * self.cell_size + self.cell_size // 2) - (self.canvas.coords(self.robot)[1] + self.cell_size // 2))
            self.master.update()
            self.master.after(500)  # Delay for robot movement

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()

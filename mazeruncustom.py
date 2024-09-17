# maze.py
import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu
from collections import deque
import random
import time
import pdb  # Import the Python Debugger

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
        # Create a frame for maze dimensions
        dimension_frame = tk.Frame(self.master)
        dimension_frame.pack(side=tk.TOP, padx=5, pady=5)

        # Input box for maze width
        self.size_x_label = tk.Label(dimension_frame, text="Maze Width:")
        self.size_x_label.pack(side=tk.LEFT, padx=5)

        self.size_x_entry = tk.Entry(dimension_frame)
        self.size_x_entry.pack(side=tk.LEFT, padx=5)

        # Input box for maze height
        self.size_y_label = tk.Label(dimension_frame, text="Maze Height:")
        self.size_y_label.pack(side=tk.LEFT, padx=5)

        self.size_y_entry = tk.Entry(dimension_frame)
        self.size_y_entry.pack(side=tk.LEFT, padx=5)

        # Dropdown for maze generation algorithm selection
        self.algorithm_var = StringVar(self.master)
        self.algorithm_var.set("Recursive Backtracking")  # Default value
        self.algorithm_menu = OptionMenu(self.master, self.algorithm_var, "Recursive Backtracking", "Prim's", "Kruskal's", "Custom")
        self.algorithm_menu.pack(side=tk.TOP, padx=5, pady=5)

        # Entry for custom algorithm input
        self.custom_algorithm_entry = tk.Entry(self.master)
        self.custom_algorithm_entry.pack(side=tk.TOP, padx=5, pady=5)
        self.custom_algorithm_entry.config(state='disabled')  # Initially disabled

        # Enable custom entry when "Custom" is selected
        def toggle_custom_entry(*args):
            if self.algorithm_var.get() == "Custom":
                self.custom_algorithm_entry.config(state='normal')
            else:
                self.custom_algorithm_entry.config(state='disabled')

        self.algorithm_var.trace("w", toggle_custom_entry)

        # Create a frame for buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack(side=tk.TOP, padx=5, pady=5)

        self.create_button = tk.Button(button_frame, text="Create Maze", command=self.create_maze)
        self.create_button.pack(side=tk.LEFT, padx=5)

        self.solve_button = tk.Button(button_frame, text="Solve Maze", command=self.solve_maze)
        self.solve_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(button_frame, text="Save Maze", command=self.save_maze)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.load_button = tk.Button(button_frame, text="Load Maze", command=self.load_maze)
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Slider for animation speed control
        self.speed_label = tk.Label(self.master, text="Animation Speed (ms):")
        self.speed_label.pack(side=tk.TOP, padx=5, pady=5)

        self.speed_slider = tk.Scale(self.master, from_=50, to=1000, resolution=50, orient=tk.HORIZONTAL)
        self.speed_slider.set(200)  # Default speed
        self.speed_slider.pack(side=tk.TOP, padx=5, pady=5)

        # Create a frame for color selection
        color_frame = tk.Frame(self.master)
        color_frame.pack(side=tk.TOP, padx=5, pady=5)

        # Color selection buttons as square boxes
        self.selected_color = 'black'  # Default color for walls

        def set_wall_color():
            self.selected_color = 'black'

        def set_start_color():
            self.selected_color = 'green'

        def set_end_color():
            self.selected_color = 'red'

        wall_color_button = tk.Button(color_frame, bg='black', width=4, height=2, command=set_wall_color)
        wall_color_button.pack(side=tk.LEFT, padx=5)

        start_color_button = tk.Button(color_frame, bg='green', width=4, height=2, command=set_start_color)
        start_color_button.pack(side=tk.LEFT, padx=5)

        end_color_button = tk.Button(color_frame, bg='red', width=4, height=2, command=set_end_color)
        end_color_button.pack(side=tk.LEFT, padx=5)

        # Labels for statistics
        self.stats_frame = tk.Frame(self.master)
        self.stats_frame.pack(side=tk.TOP, padx=5, pady=5)

        self.walls_label = tk.Label(self.stats_frame, text="Walls: 0")
        self.walls_label.pack(side=tk.LEFT, padx=5)

        self.path_length_label = tk.Label(self.stats_frame, text="Path Length: 0")
        self.path_length_label.pack(side=tk.LEFT, padx=5)

        self.time_label = tk.Label(self.stats_frame, text="Time: 0 ms")
        self.time_label.pack(side=tk.LEFT, padx=5)

    def create_maze(self):
        self.size_x = int(self.size_x_entry.get())
        self.size_y = int(self.size_y_entry.get())
        self.walls.clear()
        self.start = None
        self.end = None
        self.draw_maze()

        # Start timing for maze generation
        start_time = time.time()

        # Set a breakpoint to inspect values before maze generation
        pdb.set_trace()  # Debugger will pause here

        # Choose the maze generation algorithm
        algorithm = self.algorithm_var.get()
        if algorithm == "Recursive Backtracking":
            self.recursive_backtracking()
        elif algorithm == "Prim's":
            self.prims_algorithm()
        elif algorithm == "Kruskal's":
            self.kruskals_algorithm()
        elif algorithm == "Custom":
            custom_algorithm = self.custom_algorithm_entry.get()
            self.custom_algorithm(custom_algorithm)

        # Automatically set start and end points
        empty_cells = [(x, y) for x in range(self.size_x) for y in range(self.size_y) if (x, y) not in self.walls]
        if empty_cells:
            self.start = random.choice(empty_cells)
            empty_cells.remove(self.start)
            if empty_cells:
                self.end = random.choice(empty_cells)
            else:
                self.end = (self.size_x - 1, self.size_y - 1)
        else:
            self.start = (0, 0)
            self.end = (self.size_x - 1, self.size_y - 1)

        self.draw_maze()  # Redraw the maze after generation

        # Calculate and display statistics
        end_time = time.time()
        generation_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.walls_label.config(text=f"Walls: {len(self.walls)}")
        self.time_label.config(text=f"Time: {int(generation_time)} ms")

    def custom_algorithm(self, algorithm_input):
        # Implement the logic for the custom algorithm based on user input
        pass  # Placeholder for custom algorithm logic

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
                self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                              (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                              fill=color)

        # Draw the start point in green
        if self.start:
            x, y = self.start
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                          (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                          fill='green')  # Start point in green

        # Draw the end point in red
        if self.end:
            x, y = self.end
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                          (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                          fill='red')  # End point in red

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
        
        # Start timing for solving the maze
        start_time = time.time()

        # Set a breakpoint to inspect values before solving
        pdb.set_trace()  # Debugger will pause here

        self.path = self.bfs(self.start, self.end)
        end_time = time.time()

        # Check if the path is empty (unsolvable maze)
        if not self.path:
            messagebox.showwarning("Warning", "The maze is unsolvable.")
            return
        
        # Update statistics
        self.path_length_label.config(text=f"Path Length: {len(self.path)}")
        self.time_label.config(text=f"Time: {int((end_time - start_time) * 1000)} ms")
        
        self.animate_solution()

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
            self.master.after(self.speed_slider.get())  # Use the slider value for delay
            
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
        return path[::-1]  # Return the path in the correct order

    def has_all_colors(self):
        return self.start and self.end and len(self.walls) > 0

    def animate_solution(self):
        for step in self.path:
            x, y = step
            # Paint the box green as the robot moves
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                          (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                          fill='green')  # Paint the path green
            self.master.update()
            self.master.after(self.speed_slider.get())  # Use the slider value for delay

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
            self.master.after(self.speed_slider.get())  # Use the slider value for delay

    def recursive_backtracking(self):
        # Implementation of Recursive Backtracking algorithm
        self.walls = set()
        stack = [(0, 0)]
        visited = set(stack)

        while stack:
            x, y = stack[-1]
            neighbors = []

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size_x and 0 <= ny < self.size_y and (nx, ny) not in visited:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                # Remove the wall between (x, y) and (nx, ny)
                self.walls.add((x, y))
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

    def prims_algorithm(self):
        # Implementation of Prim's algorithm
        self.walls = set()
        grid = {(x, y): True for x in range(self.size_x) for y in range(self.size_y)}
        start = (random.randint(0, self.size_x - 1), random.randint(0, self.size_y - 1))
        walls = []

        def add_walls(x, y):
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size_x and 0 <= ny < self.size_y and (nx, ny) not in self.walls and (nx, ny) not in walls:
                    walls.append((nx, ny))

        add_walls(*start)
        self.walls.add(start)

        while walls:
            wall = random.choice(walls)
            walls.remove(wall)
            x, y = wall

            if grid[(x, y)]:
                continue

            count = 0
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size_x and 0 <= ny < self.size_y and (nx, ny) in self.walls:
                    count += 1

            if count == 1:
                self.walls.add(wall)
                grid[(x, y)] = False
                add_walls(x, y)

    def kruskals_algorithm(self):
        # Implementation of Kruskal's algorithm
        self.walls = set()
        edges = []
        for x in range(self.size_x):
            for y in range(self.size_y):
                if x < self.size_x - 1:
                    edges.append(((x, y), (x + 1, y)))
                if y < self.size_y - 1:
                    edges.append(((x, y), (x, y + 1)))

        random.shuffle(edges)
        parent = {}

        def find(v):
            if parent[v] != v:
                parent[v] = find(parent[v])
            return parent[v]

        def union(v1, v2):
            root1 = find(v1)
            root2 = find(v2)
            if root1 != root2:
                parent[root2] = root1

        for x in range(self.size_x):
            for y in range(self.size_y):
                parent[(x, y)] = (x, y)

        for edge in edges:
            v1, v2 = edge
            if find(v1) != find(v2):
                self.walls.add(v1)
                union(v1, v2)

    def save_maze(self):
        with open("saved_maze.txt", "w") as file:
            file.write(f"{self.size_x} {self.size_y}\n")  # Save dimensions
            for y in range(self.size_y):
                for x in range(self.size_x):
                    if (x, y) in self.walls:
                        file.write("1 ")  # Wall
                    else:
                        file.write("0 ")  # Empty space
                file.write("\n")
        messagebox.showinfo("Save Maze", "Maze saved successfully!")

    def load_maze(self):
        try:
            with open("saved_maze.txt", "r") as file:
                lines = file.readlines()
                self.size_x, self.size_y = map(int, lines[0].strip().split())
                self.walls.clear()
                for y in range(self.size_y):
                    row = list(map(int, lines[y + 1].strip().split()))
                    for x in range(self.size_x):
                        if row[x] == 1:
                            self.walls.add((x, y))
                self.start = None
                self.end = None
                self.draw_maze()  # Redraw the maze after loading
                messagebox.showinfo("Load Maze", "Maze loaded successfully!")
        except Exception as e:
            messagebox.showerror("Load Maze", f"Error loading maze: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()

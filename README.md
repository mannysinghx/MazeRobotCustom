# Maze Generator and Solver

This project is a simple maze generator and solver implemented in Python using Tkinter for the graphical user interface (GUI). Users can create custom mazes, place start and end points, and visualize the solving process using the breadth-first search (BFS) algorithm.

## Features

- **Custom Maze Size**: Users can input custom values for maze dimensions.
- **Color Selection**: Users can select colors to place the start point (green), end point (red), and walls (black) in the maze.
- **Maze Visualization**: The maze is visually represented in a grid format.
- **Path Visualization**: As the BFS algorithm explores the maze, it visualizes the cells being considered with yellow dots.
- **Robot Animation**: A robot-like character moves along the solution path, painting the path green as it progresses.
- **Warning Messages**: Users receive warnings if the maze is unsolvable or if all required colors are not placed.

## Requirements

- Python 3.x
- Tkinter (usually included with Python installations)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/maze-generator-solver.git
   cd maze-generator-solver
   ```

2. Run the application:
   ```bash
   python maze.py
   ```

## Usage

1. Enter the desired maze dimensions in the input boxes.
2. Click the "Create Maze" button to generate an empty maze.
3. Use the color buttons to select colors for the start point, end point, and walls.
4. Click on the maze grid to place the selected colors.
5. Click the "Solve Maze" button to visualize the solving process.

## Screenshots

![Maze Example](customMazeScreenShot.jpg)  <!-- Replace with an actual screenshot of your application -->

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by various maze generation and solving algorithms.
- Thanks to the open-source community for their contributions and resources.

# Space Bending Visualization

This project is a small program designed to help visualize the concept of space being bent by gravity. The visualization simulates a 3D grid that gets distorted as a moving mass (representing a gravitational source) travels through it. This can be a useful tool for understanding how gravity affects space in a more intuitive and interactive way.

## Features

- **3D Grid Visualization**: A wireframe grid that gets distorted to simulate the bending of space.
- **Moving Mass**: A green sphere that moves randomly within the grid, bouncing off the edges.
- **Interactive View**: Rotate the view using mouse movements to explore the 3D space from different angles.
- **Variable Transparency**: Grid lines closer to the moving mass become more opaque, providing a visual cue for the intensity of the gravitational effect.

## How to Run

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/your-username/space-bending-visualization.git
    cd space-bending-visualization
    ```

2. **Install Dependencies**:
    Ensure you have `pygame` and `PyOpenGL` installed. You can install them using pip:
    ```sh
    pip install pygame PyOpenGL
    ```

3. **Run the Program**:
    Execute the Python script to start the visualization:
    ```sh
    python grid.py
    ```

## Controls

- **Rotate View**: Click and drag with the left mouse button to rotate the view.

## Acknowledgements

This program uses `pygame` for the main loop and event handling, and `PyOpenGL` for rendering the 3D graphics.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


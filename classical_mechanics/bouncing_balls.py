import numpy as np  # Import the numpy library for numerical operations
import matplotlib.pyplot as plt  # Import the plotting library
import matplotlib.animation as animation  # Import the animation module

# Initial parameters
num_balls = 5  # Number of balls
box_size = 10  # Size of the box (10x10)
speed = 0.5  # Speed multiplier for the balls

# Generate random initial positions and velocities for the balls
np.random.seed(0)  # Seed the random number generator for reproducibility
positions = np.random.rand(num_balls, 2) * box_size  # Random positions in the box (scaled by box_size)
velocities = (np.random.rand(num_balls, 2) - 0.5) * speed  # Random velocities in range [-speed/2, speed/2]

# Print initial positions and velocities for debugging
print("Initial positions:\n", positions)
print("Initial velocities:\n", velocities)

# Function to update the positions and handle collisions
def update_positions(positions, velocities, box_size):
    # Update positions based on velocities
    next_positions = positions + velocities

    # Check for collisions with the walls and reverse velocity component if needed
    for i in range(len(next_positions)):
        if next_positions[i, 0] <= 0 or next_positions[i, 0] >= box_size:  # Collision with left or right wall
            velocities[i, 0] *= -1  # Reverse the x component of the velocity
        if next_positions[i, 1] <= 0 or next_positions[i, 1] >= box_size:  # Collision with top or bottom wall
            velocities[i, 1] *= -1  # Reverse the y component of the velocity

    # Update positions based on corrected velocities
    positions += velocities

    # Ensure positions stay within bounds
    positions = np.clip(positions, 0, box_size)

    return positions, velocities

# Example of updating positions and handling collisions
positions, velocities = update_positions(positions, velocities, box_size)

# Print updated positions and velocities for debugging
print("Updated positions:\n", positions)
print("Updated velocities:\n", velocities)

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, box_size)  # Set the x-axis limits
ax.set_ylim(0, box_size)  # Set the y-axis limits

# Create a scatter plot for the balls
scatter = ax.scatter(positions[:, 0], positions[:, 1])

# Initialization function for the animation
def init():
    scatter.set_offsets(positions)
    return scatter,

# Update function for the animation
def update(frame):
    global positions, velocities
    positions, velocities = update_positions(positions, velocities, box_size)
    scatter.set_offsets(positions)
    return scatter,

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=200, init_func=init, interval=20, blit=True)

# Show the animation
plt.show()
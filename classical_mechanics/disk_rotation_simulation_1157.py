import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants
mass_large_disk = 10 * 1  # Mass of the large disk (10m)
radius_large_disk = 3.0 * 1  # Radius of the large disk (3r)
mass_small_disk = 1  # Mass of the smaller disk (m)
radius_small_disk = 1  # Radius of the smaller disk (r)
initial_angular_velocity = 20  # Initial angular velocity of both disks (20 rad/s)

# Moment of inertia for the disks
I_large_disk = 0.5 * mass_large_disk * radius_large_disk ** 2  # Moment of inertia of the large disk
I_small_disk = 0.5 * mass_small_disk * radius_small_disk ** 2  # Moment of inertia of the small disk

# Initial angular momentum (L_initial = I_total * omega_initial)
L_initial = (I_large_disk + I_small_disk) * initial_angular_velocity  # Total initial angular momentum

# The small disk moves to the edge of the large disk
new_radius_small_disk = radius_large_disk  # New radius of the small disk (same as the large disk's radius)
I_small_disk_new = 0.5 * mass_small_disk * new_radius_small_disk ** 2  # New moment of inertia of the small disk

# New total moment of inertia
I_total_new = I_large_disk + I_small_disk_new  # Total moment of inertia after the small disk moves

# Conservation of angular momentum (L_initial = I_total_new * omega_new)
omega_new = L_initial / I_total_new  # New angular velocity after the small disk moves

# Initial kinetic energy (K0)
K0 = 0.5 * (I_large_disk + I_small_disk) * initial_angular_velocity ** 2  # Initial kinetic energy of the system

# New kinetic energy (K)
K = 0.5 * I_total_new * omega_new ** 2  # New kinetic energy of the system

# Ratio of the new kinetic energy to the initial kinetic energy
K_ratio = K / K0  # Ratio of the new kinetic energy to the initial kinetic energy

# Print the results
print(f"New angular velocity: {omega_new} rad/s")  # Print the new angular velocity
print(f"Ratio of the new kinetic energy to the initial kinetic energy: {K_ratio}")  # Print the kinetic energy ratio

# Simulation parameters
num_frames = 500  # Number of frames in the animation, increased for smoother animation
interval = 20  # Interval between frames in milliseconds

# Create figure and axes
fig, ax = plt.subplots()  # Create a figure and a set of subplots
ax.set_xlim(-radius_large_disk * 1.5, radius_large_disk * 1.5)  # Set the x-axis limits
ax.set_ylim(-radius_large_disk * 1.5, radius_large_disk * 1.5)  # Set the y-axis limits
ax.set_aspect('equal', 'box')  # Set the aspect ratio of the plot to be equal

# Plot the large disk
large_disk = plt.Circle((0, 0), radius_large_disk, color='blue', fill=False)  # Create a circle representing the large disk
ax.add_artist(large_disk)  # Add the large disk to the plot

# Plot the small disk
small_disk = plt.Circle((0, 0), radius_small_disk, color='red', fill=True)  # Create a circle representing the small disk
ax.add_artist(small_disk)  # Add the small disk to the plot

# Animation update function
def update(frame):
    # Update the position of the small disk
    new_radius = radius_small_disk + frame * (radius_large_disk - radius_small_disk) / num_frames  # Calculate the new radius of the small disk
    # Calculate the new position of the small disk
    small_disk.center = (new_radius * np.cos(omega_new * frame / num_frames), new_radius * np.sin(omega_new * frame / num_frames))
    return small_disk,

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=num_frames, interval=interval, blit=True)  # Create an animation by repeatedly calling the update function

# Display the animation
plt.show()

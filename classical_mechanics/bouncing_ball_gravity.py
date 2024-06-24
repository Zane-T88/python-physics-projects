import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initial parameters
circle_radius = 5  # Radius of the circle
num_balls = 1  # Number of balls
g = 9.81  # Acceleration due to gravity in m/s^2
dt = 0.01  # Time step for the simulation
damping_factor = 0.99  # Damping factor to simulate energy loss
ball_radius = 0.25  # Radius of each ball
boundary_margin = 0.05  # Margin to account for the visual boundary width
collision_margin = 0.01  # Margin to account for visual ball overlap

# Generate random initial positions and velocities for the balls
np.random.seed(0)
positions = (np.random.rand(num_balls, 2) - 0.5) * 2 * (circle_radius - ball_radius)
while len(positions) < num_balls:
    extra_positions = (np.random.rand(num_balls - len(positions), 2) - 0.5) * 2 * (circle_radius - ball_radius)
    extra_positions = extra_positions[np.linalg.norm(extra_positions, axis=1) < (circle_radius - ball_radius)]
    positions = np.vstack((positions, extra_positions))

velocities = (np.random.rand(num_balls, 2) - 0.5) * 10

# Print initial parameters for debugging
print("Initial positions:\n", positions)
print("Initial velocities:\n", velocities)

# Function to update the positions and velocities
def update_positions_velocities(positions, velocities, circle_radius, ball_radius, dt, damping_factor, boundary_margin, collision_margin):
    effective_radius = circle_radius - boundary_margin
    effective_diameter = 2 * ball_radius - collision_margin
    num_balls = len(positions)
    for i in range(num_balls):
        # Update velocity with gravity
        velocities[i][1] -= g * dt

        # Update position based on velocity
        next_position = positions[i] + velocities[i] * dt

        # Check for collision with the circular boundary
        if np.linalg.norm(next_position) + ball_radius >= effective_radius:
            normal = next_position / np.linalg.norm(next_position)
            velocities[i] = velocities[i] - 2 * np.dot(velocities[i], normal) * normal
            velocities[i] *= damping_factor

            # Move the ball to the boundary if it overshoots
            overshoot_distance = np.linalg.norm(next_position) + ball_radius - effective_radius
            if overshoot_distance > 0:
                next_position = normal * (effective_radius - ball_radius - overshoot_distance)

        positions[i] = next_position

    # Check for collisions between balls
    for i in range(num_balls):
        for j in range(i + 1, num_balls):
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist < effective_diameter:
                normal = (positions[i] - positions[j]) / dist
                relative_velocity = velocities[i] - velocities[j]
                velocity_along_normal = np.dot(relative_velocity, normal)

                if velocity_along_normal > 0:
                    continue

                # Calculate impulse scalar
                impulse_scalar = (2 * velocity_along_normal) / 2  # Equal mass assumption

                # Apply impulses
                velocities[i] -= impulse_scalar * normal
                velocities[j] += impulse_scalar * normal

                # Correct positions to prevent overlap
                overlap = effective_diameter - dist
                correction = normal * (overlap / 2)
                positions[i] += correction
                positions[j] -= correction

                # Additional correction to avoid overlap after impulse
                new_dist = np.linalg.norm(positions[i] - positions[j])
                if new_dist < effective_diameter:
                    correction = normal * (effective_diameter - new_dist) / 2
                    positions[i] += correction
                    positions[j] -= correction

    return positions, velocities

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(-circle_radius * 1.1, circle_radius * 1.1)
ax.set_ylim(-circle_radius * 1.1, circle_radius * 1.1)
ax.set_aspect('equal', 'box')

fig.patch.set_facecolor('black')
ax.set_facecolor('black')

circle = plt.Circle((0, 0), circle_radius, color='white', fill=False)
ax.add_artist(circle)

balls_patches = [plt.Circle(pos, ball_radius, color='red') for pos in positions]
for ball in balls_patches:
    ax.add_patch(ball)

ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

def init():
    for ball, pos in zip(balls_patches, positions):
        ball.center = pos
    return balls_patches

def update(frame):
    global positions, velocities
    positions, velocities = update_positions_velocities(positions, velocities, circle_radius, ball_radius, dt, damping_factor, boundary_margin, collision_margin)
    for ball, pos in zip(balls_patches, positions):
        ball.center = pos
    return balls_patches

ani = animation.FuncAnimation(fig, update, frames=200, init_func=init, interval=10, blit=True)
plt.show()
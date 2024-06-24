import math
import matplotlib.pyplot as plt  # Import the plotting library

# Initial parameters
v0 = 50  # initial velocity in m/s
theta = 45  # launch angle in degrees
g = 9.81  # acceleration due to gravity in m/s^2
dt = 0.01  # time step in seconds

# Convert angle to radians
theta_rad = math.radians(theta)  # Convert angle to radians for calculations

# Initialize lists to store the trajectory
t_values = [0]  # List of time values, starts with 0
x_values = [0]  # List of x-position values, starts with 0
y_values = [0]  # List of y-position values, starts with 0

# Initial conditions
t = 0  # Initial time
x = 0  # Initial x-position
y = 0  # Initial y-position

# Velocity components
vx = v0 * math.cos(theta_rad)  # Horizontal component of velocity
vy = v0 * math.sin(theta_rad)  # Vertical component of velocity

# Calculate the trajectory
while y >= 0:  # Continue the loop while the projectile is above ground
    t += dt  # Increment the time by dt
    x = vx * t  # Calculate the new x-position
    y = vy * t - 0.5 * g * t**2  # Calculate the new y-position using the equation of motion
    
    t_values.append(t)  # Add the current time to the t_values list
    x_values.append(x)  # Add the current x-position to the x_values list
    y_values.append(y)  # Add the current y-position to the y_values list
    
    print(f"t: {t}, x: {x}, y: {y}")  # Debugging print statement

# Plot the trajectory
plt.plot(x_values, y_values)  # Plot x vs y
plt.xlabel('Distance (m)')  # Label for the x-axis
plt.ylabel('Height (m)')  # Label for the y-axis
plt.title('Projectile Motion')  # Title of the plot
plt.grid(True)  # Add a grid for better readability
plt.show()  # Display the plot
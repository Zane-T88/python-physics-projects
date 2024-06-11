import numpy as np #Import the numpy library for numerical operations
import matplotlib.pyplot as plt #Import the plotting library
import matplotlib.animation as animation #Import the animation module

#Initial parameters
circle_radius = 5 #Radius of the circle equals 5
initial_position = np.array([0.0, 0.0]) #Start at the center of the circle
initial_velocity = np.array([2.0, 5.0]) #Initial velocity of the ball
g = 9.81 #Acceleration due to gravity in m/s^2
dt = 0.01 #Time step for the simulation
damping_factor = 0.99 #Damping factor to simulate energy loss

#Generate random initial positons and velocities for the balls
np.random.seed(0) #Seed the random number generator for reproducibility
positions = (np.random.rand(num_balls, 2) - 0.5) * (circle_radius)

#Print initial parameters for debugging
print("Intitial position:\n", initial_position)
print("Initial velocity:\n", initial_velocity)

#Function to update the position and velocity
def update_position_velocity(position, velocity, circle_radius, dt, damping_factor):
    #Update velcoity with gravity
    velocity[1] -= g * dt #Gravity affects the y-component of velocity

    #Update position based on velocity
    next_position = position + velocity * dt

    #Check for collision with circular boundary
    if np.linalg.norm(next_position) >= circle_radius:
        #Reflect the velocity vector
        normal = next_position / np.linalg.norm(next_position) #Unit vector in the direction of boundary
        velocity = velocity - 2 * np.dot(velocity, normal) * normal #Reflect velocity
        velocity *= damping_factor #Apply damping factor

        #Move the ball to the boundary if it overshoots
        next_position = position + velocity * dt
        if np.linalg.norm(next_position) >= circle_radius: 
            next_postion = normal * circle_radius

    return next_position, velocity 

#Example of updating position and velocity
position = initial_position
velocity = initial_velocity

#Update position adn velocity fo rone time step
position, velocity, = update_position_velocity(position, velocity, circle_radius, dt, damping_factor)

#Print updated position and velocity for debugging
print("Updated position:\n", position)
print("Updated velocity:\n", velocity)

#Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(-circle_radius * 1.1, circle_radius * 1.1) #Set the x-axis limits
ax.set_ylim(-circle_radius * 1.1, circle_radius * 1.1) #Set the y-axis limits
ax.set_aspect('equal', 'box') #Ensure the aspect ration is equal

#Set the background color to black
fig.patch.set_facecolor('black') #Set figure background color
ax.set_facecolor('black')


#Create a circle to represent the boundary
circle = plt.Circle((0,0), circle_radius, color='white', fill=False)
ax.add_artist(circle)

#Create a scatter plot for the ball
ball, = ax.plot([], [], 'o', color='red')

#Hide the axis borders and ticks
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

#Initialization function for the animation
def init():
    ball.set_data(initial_position[0], initial_position[1])
    return ball,

#Update function for the animation
def update(frame):
    global position, velocity
    position, velocity = update_position_velocity(position, velocity, circle_radius, dt, damping_factor)
    ball.set_data(position[0], position[1])
    return ball, 

#Create the animation
ani = animation.FuncAnimation(fig, update, frames=200, init_func=init, interval=20, blit=True)

#Show the animation
plt.show()

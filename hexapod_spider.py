import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

class SpiderRobot:
    def __init__(self, body_radius, leg_length):
        self.body_radius = body_radius
        self.leg_length = leg_length
        self.leg_positions = []
        for i in range(6):
            x = body_radius * np.cos(i * np.pi / 3)
            y = body_radius * np.sin(i * np.pi / 3)
            z = 0
            position = [x, y, z]
            self.leg_positions.append(position)
           
        self.joint1_angles = np.zeros(6) 
        self.joint2_angles = np.zeros(6) 

    def get_leg_points(self, leg_index):
        leg_position = self.leg_positions[leg_index]
        joint1_angle = self.joint1_angles[leg_index]
        joint2_angle = self.joint2_angles[leg_index]
        x = [
            leg_position[0],
            leg_position[0] + self.leg_length/2 * np.cos(joint1_angle),
            leg_position[0] + self.leg_length/2 * np.cos(joint1_angle) + self.leg_length/2 * np.cos(joint1_angle + joint2_angle)
        ]
        y = [
            leg_position[1],
            leg_position[1] + self.leg_length/2 * np.sin(joint1_angle),
            leg_position[1] + self.leg_length/2 * np.sin(joint1_angle) + self.leg_length/2 * np.sin(joint1_angle + joint2_angle)
        ]
        z = [
             leg_position[2],
            2,
            -2
        ]
        return x, y, z

    def get_end_effector_position(self):
        positions = []
        for leg_index in range(6):
            leg_position = self.leg_positions[leg_index]
            joint1_angle = self.joint1_angles[leg_index]
            joint2_angle = self.joint2_angles[leg_index]
            end_effector_x = (
                leg_position[0] + self.leg_length/2 * np.cos(joint1_angle) + self.leg_length/2 * np.cos(joint1_angle + joint2_angle)
            )
            end_effector_y = (
                leg_position[1] + self.leg_length/2 * np.sin(joint1_angle) + self.leg_length/2 * np.sin(joint1_angle + joint2_angle)
            )
            end_effector_z = -2  # Festgelegte Z-Koordinate
            positions.append([end_effector_x, end_effector_y, end_effector_z])
        return positions

    def plot_spider(self, ax):
        hexagon_x = []
        hexagon_y = []
        hexagon_z = []
        for position in self.leg_positions:
            hexagon_x.append(position[0])
            hexagon_y.append(position[1])
            hexagon_z.append(position[2])

        hexagon_x.append(self.leg_positions[0][0])
        hexagon_y.append(self.leg_positions[0][1])
        hexagon_z.append(self.leg_positions[0][2])

        ax.plot(hexagon_x, hexagon_y, hexagon_z, color='blue')

        for leg_index in range(6):
            x, y, z = self.get_leg_points(leg_index)
            ax.plot(x, y, z, color='red')

        end_effector_positions = self.get_end_effector_position()
        end_effector_x = []
        end_effector_y = []
        end_effector_z = []

        for position in end_effector_positions:
            end_effector_x.append(position[0])
            end_effector_y.append(position[1])
            end_effector_z.append(position[2])

        ax.scatter(end_effector_x, end_effector_y, end_effector_z, color='green', marker='o')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        return ax

    def calculate_jacobian(self):
        jacobian = np.zeros((2, 6))
        for leg_index in range(6):
            leg_position = self.leg_positions[leg_index]
            joint1_angle = self.joint1_angles[leg_index]
            joint2_angle = self.joint2_angles[leg_index]
            jacobian[0, leg_index] = -self.leg_length/2 * np.sin(joint1_angle) - self.leg_length/2 * np.sin(joint1_angle + joint2_angle)
            jacobian[1, leg_index] = self.leg_length/2 * np.cos(joint1_angle) + self.leg_length/2 * np.cos(joint1_angle + joint2_angle)
        return jacobian

body_radius = 1.0
leg_length = 1.0
spider = SpiderRobot(body_radius, leg_length)

num_frames = 220

def update(frame):
    t = frame / num_frames

    # Gelenkwinkel für die ersten drei Beine, die sich zuerst bewegen
    joint1_angles_1 = [
        np.sin(t*60),            # Mitte Rechts
        np.cos(t*60),            # Hinten Rechts
        -np.sin(t*60) + np.pi,   # Hinten links (gespiegelt)
    ]
    joint2_angles_1 = [
        np.sin(t),               # Mitte Rechts
        np.cos(t),               # Hinten Rechts
        -np.cos(t),              # Hinten links (gespiegelt)
    ]

    # Gelenkwinkel für die anderen drei Beine, die sich anschließend bewegen
    joint1_angles_2 = [
        -np.cos(t*60) + np.pi,   # Mitte Links (gespiegelt)
        -np.sin(t*60) + np.pi,   # Vorne Links (gespiegelt)
        np.cos(t*60)             # Vorne Rechts
    ]
    joint2_angles_2 = [
        -np.sin(t),              # Mitte Links (gespiegelt)
        -np.sin(t),              # Vorne Links (gespiegelt)
        np.cos(t)                # Vorne rechts
    ]

    spider.joint1_angles = joint1_angles_1 + joint1_angles_2
    spider.joint2_angles = joint2_angles_1 + joint2_angles_2

    ax.clear()
    spider.plot_spider(ax)
    ax.set_title(f'Frame {frame+1}/{num_frames}')

    # Calculate and display the Jacobian matrix
    jacobian = spider.calculate_jacobian()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
animation = FuncAnimation(fig, update, frames=num_frames, interval=100)


plt.show()

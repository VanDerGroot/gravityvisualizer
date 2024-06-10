import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Function to distort space around a central mass
def distort_space(position, center, strength):
    r = np.linalg.norm(position - center)
    if r == 0:
        return position
    distortion = strength / (r ** 2)
    return center + (position - center) * (1 - distortion)

# Function to calculate the alpha value based on distance
def calculate_alpha(point, center, max_distance):
    distance = np.linalg.norm(point - center)
    if distance > max_distance:
        return 0.1
    return 0.1 + (1.0 - 0.1) * (1 - distance / max_distance)

# Create the 3D grid points
grid_size = 10
spacing = 1.0
strength = 0.5  # Strength of the gravitational distortion
max_distance = 3 * spacing  # Maximum distance for the effect

x = np.linspace(-grid_size/2, grid_size/2, grid_size) * spacing
y = np.linspace(-grid_size/2, grid_size/2, grid_size) * spacing
z = np.linspace(-grid_size/2, grid_size/2, grid_size) * spacing

def draw_grid(center):
    for i in range(grid_size):
        for j in range(grid_size):
            glBegin(GL_LINE_STRIP)
            for k in range(grid_size):
                point = np.array([x[i], y[j], z[k]])
                distorted_point = distort_space(point, center, strength)
                alpha = calculate_alpha(distorted_point, center, max_distance)
                glColor4f(0.678, 0.847, 0.902, alpha)  # Light blue color with variable alpha
                glVertex3fv(distorted_point)
            glEnd()
            glBegin(GL_LINE_STRIP)
            for k in range(grid_size):
                point = np.array([x[i], y[k], z[j]])
                distorted_point = distort_space(point, center, strength)
                alpha = calculate_alpha(distorted_point, center, max_distance)
                glColor4f(0.678, 0.847, 0.902, alpha)
                glVertex3fv(distorted_point)
            glEnd()
            glBegin(GL_LINE_STRIP)
            for k in range(grid_size):
                point = np.array([x[k], y[i], z[j]])
                distorted_point = distort_space(point, center, strength)
                alpha = calculate_alpha(distorted_point, center, max_distance)
                glColor4f(0.678, 0.847, 0.902, alpha)
                glVertex3fv(distorted_point)
            glEnd()

def draw_sphere(radius, lats, longs):
    for i in range(lats):
        lat0 = np.pi * (-0.5 + float(i) / lats)
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        
        lat1 = np.pi * (-0.5 + float(i+1) / lats)
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
        
        glBegin(GL_QUAD_STRIP)
        for j in range(longs+1):
            lng = 2 * np.pi * float(j) / longs
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(x * zr0 * radius, y * zr0 * radius, z0 * radius)
            glVertex3f(x * zr1 * radius, y * zr1 * radius, z1 * radius)
        glEnd()

def draw_moving_object(center):
    glPushMatrix()
    glTranslatef(center[0], center[1], center[2])
    glColor3f(0.0, 1.0, 0.0)  # Green color for the central mass
    draw_sphere(0.3, 20, 20)  # Draw a solid sphere
    glPopMatrix()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20)
    
    center_position = -grid_size/2 * spacing - 1
    end_position = grid_size/2 * spacing + 1
    step = 0.1
    direction = 1

    # Enable blending for transparency
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Variables to handle mouse rotation
    rotate_x = 0
    rotate_y = 0
    mouse_down = False
    last_pos = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
                    last_pos = pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
            elif event.type == MOUSEMOTION:
                if mouse_down:
                    current_pos = pygame.mouse.get_pos()
                    dx = current_pos[0] - last_pos[0]
                    dy = current_pos[1] - last_pos[1]
                    rotate_x += dy
                    rotate_y += dx
                    last_pos = current_pos

        center_position += step * direction
        if center_position > end_position or center_position < -end_position:
            direction *= -1

        center = np.array([center_position, 0, 0])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Apply rotations based on mouse movements
        glPushMatrix()
        glRotatef(rotate_x, 1, 0, 0)
        glRotatef(rotate_y, 0, 1, 0)
        
        draw_grid(center)
        draw_moving_object(center)
        
        glPopMatrix()
        
        pygame.display.flip()
        pygame.time.wait(10)

main()

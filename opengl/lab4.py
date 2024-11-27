import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


def generate_flag_grid(width, height, segments_w, segments_h):
    vertices = []
    indices = []
    dx = width / segments_w
    dy = height / segments_h

    for j in range(segments_h + 1):
        for i in range(segments_w + 1):
            x = i * dx
            y = j * dy
            z = 0
            vertices.append([x, y, z])

    for j in range(segments_h):
        for i in range(segments_w):
            top_left = j * (segments_w + 1) + i
            top_right = top_left + 1
            bottom_left = top_left + (segments_w + 1)
            bottom_right = bottom_left + 1

            indices.append([top_left, bottom_left, bottom_right])
            indices.append([top_left, bottom_right, top_right])

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

pygame.init()
screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
pygame.display.set_caption("флаг")

glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (800 / 600), 0.1, 50.0)
glTranslatef(-2.0, -1.5, -5)

flag_width = 4
flag_height = 2
segments_w = 20
segments_h = 10
vertices, indices = generate_flag_grid(flag_width, flag_height, segments_w, segments_h)
gluLookAt(1, 1, 3, 0, 0, 0, 0, 1, 0)
time = 0.0

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glColor3f(0.5, 0.5, 0.5)

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)

    for tri in indices:
        for vertex_id in tri:
            x, y, z = vertices[vertex_id]
            z = np.sin(x * 2 + time) * 0.2
            glVertex3f(x + 0.1, y, z)
    glEnd()

    time += 0.05

    pygame.display.flip()
    pygame.time.wait(16)

pygame.quit()

import pygame
import math
from pygame.locals import DOUBLEBUF, OPENGL, QUIT
from OpenGL.GL import (
    glEnable,
    glClear,
    GL_DEPTH_TEST,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_QUADS,
    glBegin,
    glEnd,
    glVertex3f,
    glTranslatef,
    glColor3f,
)
from OpenGL.GLU import gluPerspective, gluLookAt

pygame.init()
screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Флаг")

glEnable(GL_DEPTH_TEST)
gluPerspective(45, (800 / 600), 0.1, 50.0)
glTranslatef(-2.0, -0.5, -5)
gluLookAt(1, 1, 3, 0, 0, 0, 0, 1, 0)

flag_width = 2
segments_w = 10
dx = flag_width / segments_w

vertices = []
for i in range(segments_w + 1):
    x = i * dx
    vertices.append((x, 0, 0))
    vertices.append((x, 1, 0))

rectangles = []
for i in range(segments_w):
    bottom_left = i * 2
    bottom_right = bottom_left + 2
    top_left = bottom_left + 1
    top_right = bottom_right + 1
    rectangles.append([bottom_left, bottom_right, top_right, top_left])

time = 0.0
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)

    glBegin(GL_QUADS)
    for rect in rectangles:
        for vertex_id in rect:
            x, y, z = vertices[vertex_id]
            z = 0.2 * math.sin(x * 2 + time)
            glVertex3f(x, y, z)
    glEnd()

    time += 0.05

    pygame.display.flip()
    pygame.time.wait(16)

pygame.quit()

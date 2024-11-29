import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT
from OpenGL.GL import (
    glEnable,
    glClear,
    GL_DEPTH_TEST,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_QUAD_STRIP,
    GL_TRIANGLE_FAN,
    glBegin,
    glEnd,
    glVertex3f,
    glRotatef,
    glTranslatef,
    glColor3f,
)
from OpenGL.GLU import gluPerspective
import numpy as np

radius = 1.0
height = 2.0
slices = 50


def draw_cylinder():
    glBegin(GL_QUAD_STRIP)
    for i in range(slices + 1):
        angle = 2 * np.pi * i / slices
        x = np.cos(angle) * radius
        z = np.sin(angle) * radius

        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(x, height / 2, z)

        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(x, -height / 2, z)
    glEnd()

    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(0.0, height / 2, 0.0)
    for i in range(slices + 1):
        angle = 2 * np.pi * i / slices
        x = np.cos(angle) * radius
        z = np.sin(angle) * radius

        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(x, height / 2, z)
    glEnd()

    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(0.0, -height / 2, 0.0)
    for i in range(slices + 1):
        angle = 2 * np.pi * i / slices
        x = np.cos(angle) * radius
        z = np.sin(angle) * radius

        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(x, -height / 2, z)
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    glEnable(GL_DEPTH_TEST)

    # Главный цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        glRotatef(1, 3, 1, 1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cylinder()
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()


if __name__ == "__main__":
    main()

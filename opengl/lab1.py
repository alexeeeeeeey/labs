import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT
from OpenGL.GL import (
    glClearColor,
    glEnable,
    glClear,
    GL_DEPTH_TEST,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_PROJECTION,
    GL_MODELVIEW,
    GL_QUADS,
    glLoadIdentity,
    glMatrixMode,
    glBegin,
    glEnd,
    glVertex3f,
    glRotatef,
    glColor3f,
)
from OpenGL.GLU import gluPerspective, gluLookAt


def init_pygame(width, height):
    pygame.init()
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)


def init_opengl(width, height):
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / height, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def handle_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()


def draw_cube():
    vertices = [
        (1.0, 1.0, -1.0),
        (-1.0, 1.0, -1.0),
        (-1.0, 1.0, 1.0),
        (1.0, 1.0, 1.0),
        (1.0, -1.0, 1.0),
        (-1.0, -1.0, 1.0),
        (-1.0, -1.0, -1.0),
        (1.0, -1.0, -1.0),
    ]

    colors = [
        (1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0),
        (1.0, 0.5, 0.0),
        (0.5, 0.0, 1.0),
        (1.0, 1.0, 1.0),
        (0.0, 1.0, 1.0),
    ]

    faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [1, 2, 5, 6],
        [0, 3, 4, 7],
        [2, 3, 4, 5],
        [0, 1, 6, 7],
    ]

    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3f(*colors[i])
        for vertex in face:
            glVertex3f(*vertices[vertex])
    glEnd()


def main():
    width, height = 800, 600
    init_pygame(width, height)
    init_opengl(width, height)

    angle = 0

    while True:
        handle_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        gluLookAt(3, 3, 3, 0, 0, 0, 0, 0, 1)

        glRotatef(angle, 0, 0, 1)
        glRotatef(angle, 0, 1, 0)
        glRotatef(angle, 1, 0, 0)

        draw_cube()

        pygame.display.flip()
        pygame.time.wait(10)

        angle += 1
        if angle >= 360:
            angle = 0


if __name__ == "__main__":
    main()

import pygame
import os
import math
import pathlib
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import (
    glClearColor,
    glEnable,
    glClear,
    GL_DEPTH_TEST,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_PROJECTION,
    GL_MODELVIEW,
    glBindTexture,
    glTexParameteri,
    glLoadIdentity,
    glTexImage2D,
    GL_REPEAT,
    glGenTextures,
    glRotatef,
    GL_LINEAR,
    GL_TEXTURE_MAG_FILTER,
    GL_RGBA,
    GL_TEXTURE_MIN_FILTER,
    glEnd,
    glBegin,
    GL_TRIANGLE_STRIP,
    glTexCoord2f,
    GL_TRIANGLE_FAN,
    glVertex3f,
    GL_UNSIGNED_BYTE,
    GL_TEXTURE_WRAP_T,
    GL_TEXTURE_2D,
    GL_TEXTURE_WRAP_S,
    glMatrixMode,
)
from OpenGL.GLU import (
    gluPerspective,
    gluLookAt,
)


def load_texture(texture_path):
    texture_surface = pygame.image.load(texture_path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", True)
    width, height = texture_surface.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        width,
        height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        texture_data,
    )
    glBindTexture(GL_TEXTURE_2D, 0)
    return texture_id


def draw_cylinder(can_texture_id, can_up_down_texture_id):
    radius = 1
    height = 2
    segments = 50

    # боковая часть
    glBindTexture(GL_TEXTURE_2D, can_texture_id)
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        glTexCoord2f(i / segments, 1)
        glVertex3f(x, y, height)

        glTexCoord2f(i / segments, 0)
        glVertex3f(x, y, -height)
    glEnd()

    # верхнюя крышка
    glBindTexture(GL_TEXTURE_2D, can_up_down_texture_id)
    glBegin(GL_TRIANGLE_FAN)
    glTexCoord2f(0.5, 0.75)
    glVertex3f(0.0, 0.0, height)
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glTexCoord2f(0.5 + math.cos(angle) * 0.375,
                     0.75 + math.sin(angle) * 0.175)
        glVertex3f(x, y, height)
    glEnd()

    # дно
    glBegin(GL_TRIANGLE_FAN)
    glTexCoord2f(0.5, 0.25)
    glVertex3f(0.0, 0.0, -height)
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glTexCoord2f(0.5 + math.cos(angle) * 0.375,
                     0.25 + math.sin(angle) * 0.175)
        glVertex3f(x, y, -height)
    glEnd()


pygame.init()

width = 800
height = 600

display = (width, height)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glClearColor(0, 0, 0, 1.0)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glEnable(GL_DEPTH_TEST)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()

gluPerspective(45.0, width / height, 0.1, 100.0)

glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

can_texture_id = load_texture(
    os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        "textures",
        "lab6",
        "can_coca_loca.png",
    )
)

can_up_down_texture_id = load_texture(
    os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        "textures",
        "lab6",
        "top_bot_can.png",
    )
)

glEnable(GL_TEXTURE_2D)

rotation_angle = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    gluLookAt(3, 6, 12, 0, 0, 0, 0, 0, 1)

    glRotatef(rotation_angle, 1, 1, 0)

    draw_cylinder(can_texture_id, can_up_down_texture_id)

    pygame.display.flip()
    pygame.time.wait(10)

    rotation_angle += 1

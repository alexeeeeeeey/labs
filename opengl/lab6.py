import pygame
import os
import math
import pathlib
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import (
    glCullFace,
    GL_CULL_FACE,
    GL_BACK,
    glClearColor,
    glEnable,
    glClear,
    GL_DEPTH_TEST,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    glNormal3f,
    GL_PROJECTION,
    GL_MODELVIEW,
    glBindTexture,
    glTexParameteri,
    glLoadIdentity,
    glTexImage2D,
    glLightfv,
    GL_SPECULAR,
    GL_AMBIENT,
    GL_DIFFUSE,
    GL_POSITION,
    GL_REPEAT,
    GL_LIGHTING,
    GL_LIGHT0,
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


def init_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    light_position = [1, 1, 1, 0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_ambient = [0.2, 0.2, 0.2, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)


def draw_cylinder(can_texture_id, can_up_down_texture_id):
    radius = 1
    height = 2
    segments = 50

    # Боковая часть
    glBindTexture(GL_TEXTURE_2D, can_texture_id)
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        glNormal3f(math.cos(angle), math.sin(angle), 0)

        glTexCoord2f(i / segments, 1)
        glVertex3f(x, y, height)

        glTexCoord2f(i / segments, 0)
        glVertex3f(x, y, -height)
    glEnd()

    # Верхняя крышка
    glBindTexture(GL_TEXTURE_2D, can_up_down_texture_id)
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0.0, 0.0, 1.0)
    glTexCoord2f(0.5, 0.75)
    glVertex3f(0.0, 0.0, height)
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glTexCoord2f(
            0.5 + math.cos(angle) * 0.375, 0.75 + math.sin(angle) * 0.175
        )
        glVertex3f(x, y, height)
    glEnd()

    # Дно
    glBindTexture(GL_TEXTURE_2D, can_up_down_texture_id)
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0.0, 0.0, -1.0)
    glTexCoord2f(0.5, 0.25)
    glVertex3f(0.0, 0.0, -height)
    for i in range(segments, -1, -1):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glTexCoord2f(
            0.5 + math.cos(angle) * 0.375, 0.25 + math.sin(angle) * 0.175
        )
        glVertex3f(x, y, -height)
    glEnd()


def init_pygame(width, height):
    pygame.init()

    display = (width, height)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)


def init_opengl(width, height):
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, width / height, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_TEXTURE_2D)


init_pygame(800, 600)
init_opengl(800, 600)


def main():
    init_lighting()
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
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


if __name__ == "__main__":
    main()

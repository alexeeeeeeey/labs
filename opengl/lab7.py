import pygame
import os
import pathlib
import math
from pygame.locals import DOUBLEBUF, OPENGL, K_w, K_d, K_s, K_a, K_LSHIFT, K_SPACE
from OpenGL.GL import (
    glCullFace, GL_BACK, GL_CULL_FACE,
    glClearColor, glEnable, glClear, glBindTexture, glTexParameteri, glTexImage2D, glNormal3f, glBegin, glEnd,
    GL_DEPTH_TEST, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_QUADS, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, glVertex3f,
    glTexCoord2f, glLightfv, GL_LIGHTING, GL_LIGHT0, GL_TEXTURE_2D, glGenTextures, GL_REPEAT, GL_LINEAR, GL_RGBA,
    GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_POSITION, GL_DIFFUSE,
    GL_AMBIENT, GL_SPECULAR, glLoadIdentity, glMatrixMode, GL_MODELVIEW, GL_PROJECTION, glTranslatef, glPopMatrix, glPushMatrix,
    GL_UNSIGNED_BYTE, glDisable, glRotatef
)
from OpenGL.GLU import gluPerspective


def load_texture(texture_path):
    texture_surface = pygame.image.load(texture_path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", True)
    width, height = texture_surface.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data
    )
    glBindTexture(GL_TEXTURE_2D, 0)
    return texture_id


def draw_walls(texture_id, size, height):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Левая стена
    glBegin(GL_QUADS)
    glNormal3f(1.0, 0.0, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-size, 0, -size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-size, height, -size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-size, height, size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-size, 0, size)
    glEnd()

    # Задняя стена
    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(size, 0, -size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(size, height, -size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-size, height, -size)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-size, 0, -size)
    glEnd()

    # Правая стена
    glBegin(GL_QUADS)
    glNormal3f(-1.0, 0.0, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(size, 0, size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(size, height, size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(size, height, -size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(size, 0, -size)
    glEnd()

    glDisable(GL_TEXTURE_2D)


def draw_floor(texture_id, size):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin(GL_QUADS)
    glNormal3f(0.0, -1.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-size, 0, size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(size, 0, size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(size, 0, -size)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-size, 0, -size)
    glEnd()

    glDisable(GL_TEXTURE_2D)


def draw_cylinder(can_texture_id, can_top_bottom_texture_id):
    radius = 0.2
    height = 0.6
    segments = 50

    # Боковая часть
    glBindTexture(GL_TEXTURE_2D, can_texture_id)
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        glNormal3f(x / radius, y / radius, 0.0)
        glTexCoord2f(i / segments, 1)
        glVertex3f(x, y, height)
        glTexCoord2f(i / segments, 0)
        glVertex3f(x, y, 0)
    glEnd()

    # Верхняя крышка
    glBindTexture(GL_TEXTURE_2D, can_top_bottom_texture_id)
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

    # Нижняя крышка
    glBindTexture(GL_TEXTURE_2D, can_top_bottom_texture_id)
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0.0, 1.0, 0.0)
    glTexCoord2f(0.5, 0.25)
    glVertex3f(0.0, 0.0, 0)
    for i in range(segments, -1, -1):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glTexCoord2f(
            0.5 + math.cos(angle) * 0.375, 0.25 + math.sin(angle) * 0.175
        )
        glVertex3f(x, y, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)


def init_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    light_position = [0, -1, 0, 1]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_ambient = [1, 1, 1, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)


def init_pygame(width, height):
    pygame.init()
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)


def init_opengl(width, height):
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, width / height, 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_TEXTURE_2D)


def handle_camera_movement():
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        glTranslatef(0, 0, 0.1)
    if keys[K_s]:
        glTranslatef(0, 0, -0.1)
    if keys[K_a]:
        glTranslatef(0.1, 0, 0)
    if keys[K_d]:
        glTranslatef(-0.1, 0, 0)
    if keys[K_LSHIFT]:
        glTranslatef(0, 0.1, 0)
    if keys[K_SPACE]:
        glTranslatef(0, -0.1, 0)


def main():
    init_pygame(800, 600)
    init_opengl(800, 600)
    init_lighting()
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glTranslatef(0, 0, -3)
    glTranslatef(0, -0.5, 0)

    brick_texture = load_texture(os.path.join(pathlib.Path(__file__).parent.resolve(), "textures", "lab7", "brick.jpg"))
    grass_texture = load_texture(os.path.join(pathlib.Path(__file__).parent.resolve(), "textures", "lab7", "grass.jpg"))
    can_side_texture = load_texture(os.path.join(pathlib.Path(__file__).parent.resolve(), "textures", "lab6", "can_coca_loca.png"))
    can_top_bottom_texture = load_texture(os.path.join(pathlib.Path(__file__).parent.resolve(), "textures", "lab6", "top_bot_can.png"))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        handle_camera_movement()

        draw_walls(brick_texture, 1, 1)
        draw_floor(grass_texture, 1)

        glPushMatrix()
        glTranslatef(0.5, 0.25, 0)
        glRotatef(90, -1, 0, 0)
        draw_cylinder(can_side_texture, can_top_bottom_texture)
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()

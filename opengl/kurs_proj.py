import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import time

WIDTH, HEIGHT = 800, 800

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

def draw_circle(radius, segments=100):
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex2f(x, y)
    glEnd()

def draw_hand(length, angle, width=0.02):
    glPushMatrix()
    glRotatef(angle, 0, 0, 1)
    glBegin(GL_QUADS)
    glVertex2f(-width / 2, 0)
    glVertex2f(width / 2, 0)
    glVertex2f(width / 2, length)
    glVertex2f(-width / 2, length)
    glEnd()
    glPopMatrix()

def draw_box(x, y, z, size_x, size_y, size_z, texture_id):
    glPushMatrix()
    vertices = [
        (x - size_x, y - size_y, z - size_z),
        (x + size_x, y - size_y, z - size_z),
        (x + size_x, y + size_y, z - size_z),
        (x - size_x, y + size_y, z - size_z),
        (x - size_x, y - size_y, z + size_z),
        (x + size_x, y - size_y, z + size_z),
        (x + size_x, y + size_y, z + size_z),
        (x - size_x, y + size_y, z + size_z)
    ]

    normals = [
        (0, 0, 1),
        (0, 0, -1),
        (0, -1, 0),
        (0, 1, 0),
        (-1, 0, 0),
        (1, 0, 0)
    ]

    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (2, 3, 7, 6),
        (4, 7, 3, 0),
        (1, 2, 6, 5)
    ]

    tex_coords = [
        (0, 0), (1, 0), (1, 1), (0, 1)
    ]

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin(GL_QUADS)
    material_diffuse = [0.6, 0.3, 0.1, 0.0]
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    for i, face in enumerate(faces):
        glNormal3fv(normals[i])
        for j, vertex in enumerate(face):
            if texture_id:
                glTexCoord2fv(tex_coords[j])
            glVertex3fv(vertices[vertex])
    glEnd()

    glDisable(GL_TEXTURE_2D)

    glPopMatrix()

def draw_clock():
    glPushMatrix()
    material_diffuse = [1, 1, 1, 1]
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glTranslatef(0, 0, 1.001)
    draw_circle(1.0)

    for i in range(12):
        angle = math.radians(360 * i / 12)
        x1, y1 = 1.0 * 0.9 * math.cos(angle), 1.0 * 0.9 * math.sin(angle)
        x2, y2 = 1.0 * math.cos(angle), 1.0 * math.sin(angle)
        glBegin(GL_LINES)
        glNormal3f(0, 0, 1)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()

    for i in range(60):
        angle = math.radians(360 * i / 60)
        x1, y1 = 1.0 * 0.95 * math.cos(angle), 1.0 * 0.95 * math.sin(angle)
        x2, y2 = 1.0 * math.cos(angle), 1.0 * math.sin(angle)
        glBegin(GL_LINES)
        glNormal3f(0, 0, 1)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()

    t = time.time()
    seconds = t % 60
    minutes = (t // 60) % 60
    hours = (t // 3600) % 12

    second_angle = -360 * seconds / 60
    minute_angle = -360 * (minutes + seconds / 60) / 60
    hour_angle = -360 * (hours + minutes / 60) / 12

    glNormal3f(0, 0, 1)
    draw_hand(0.8, second_angle, width=0.01)

    glNormal3f(0, 0, 1)
    draw_hand(0.7, minute_angle, width=0.02)

    glNormal3f(0, 0, 1)
    draw_hand(0.5, hour_angle, width=0.03)
    glPopMatrix()

def init_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    light_position = [0, -1, 0, 1]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_ambient = [1.5, 1.5, 1.5, 1.0]
    light_specular = [1.5, 1.5, 1.5, 1.0]

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

def draw_pendulum(x, y, z, texture_id):
    angle = math.sin(time.time() * 2) * 10
    glPushMatrix()
    glTranslatef(x, y, z)

    # first circle
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0, 0, -10)
    glTexCoord2f(0.5, 0.5)
    glVertex2f(0, 0)
    for i in range(101):
        angle1 = 2 * math.pi * i / 100
        x = 0.1 * math.cos(angle1)
        y = 0.1 * math.sin(angle1)
        glTexCoord2f(0.5 + 0.5 * math.cos(angle1), 0.5 + 0.5 * math.sin(angle1))
        glVertex2f(x, y)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

    # rod    
    glRotatef(angle, 0, 0, 1)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin(GL_QUADS)
    glNormal3f(0, 0, -10)
    glTexCoord2f(0, 0)
    glVertex3f(-0.1, -2, 0)
    glTexCoord2f(1, 0)
    glVertex3f(0.1, -2, 0)
    glTexCoord2f(1, 1)
    glVertex3f(0.1, 0, 0)
    glTexCoord2f(0, 1)
    glVertex3f(-0.1, 0, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)

    # second circle
    glTranslatef(0, -2, 0.01)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0, 0, -10)
    glTexCoord2f(0.5, 0.5)
    glVertex2f(0, 0)
    for i in range(101):
        angle = 2 * math.pi * i / 100
        x = 0.2 * math.cos(angle)
        y = 0.2 * math.sin(angle)
        glTexCoord2f(0.5 + 0.5 * math.cos(angle), 0.5 + 0.5 * math.sin(angle))
        glVertex2f(x, y)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

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
    if keys[K_LEFT]:
        glRotatef(1, 0, 1, 0)
    if keys[K_RIGHT]:
        glRotatef(1, 0, -1, 0)
    if keys[K_UP]:
        glRotatef(1, 1, 0, 0)
    if keys[K_DOWN]:
        glRotatef(1, -1, 0, 0)

def main():
    init_pygame(WIDTH, HEIGHT)
    init_opengl(WIDTH, HEIGHT)

    glTranslatef(0, 3, -15)

    init_lighting()
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    wood_texture = load_texture(r"opengl\textures\kurs_proj\wood.jpg")
    gold_texture = load_texture(r"opengl\textures\kurs_proj\gold.jpg")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_box(0, 0, 0, 1, 1, 1, wood_texture)
        draw_box(0, -3, 0, 1, 2, 0.5, wood_texture)
        draw_box(0, -5.5, 0, 1, 0.5, 1, wood_texture)
        draw_pendulum(0, -2, 0.51, gold_texture)
        draw_clock()

        handle_camera_movement()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

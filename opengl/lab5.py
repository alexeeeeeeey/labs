import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

# Константы
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Параметры солнечной системы
PLANETS = [
    {"radius": 0.1, "distance": 1, "speed": 0.2, "color": (1.0, 1.0, 0.0)},
    {"radius": 0.2, "distance": 2, "speed": 0.15, "color": (1.0, 0.3, 0.0)},
    {"radius": 0.3, "distance": 3, "speed": 0.1, "color": (0.2, 0.5, 1.0)},
    {"radius": 0.4, "distance": 5, "speed": 0.07, "color": (0.8, 0.4, 0.2)},
    {"radius": 1.0, "distance": 8, "speed": 0.03, "color": (1.0, 1.0, 0.5)},
    {"radius": 0.8, "distance": 12, "speed": 0.02, "color": (0.7, 0.7, 0.7)},
    {"radius": 0.7, "distance": 15, "speed": 0.01, "color": (0.6, 0.6, 0.6)},
    {"radius": 0.6, "distance": 18, "speed": 0.008, "color": (0.2, 0.3, 0.8)},
]

MOONS = [
    {"radius": 0.05, "distance": 0.3, "speed": 2, "planet": 2},
    {"radius": 0.2, "distance": 1.5, "speed": 0.5, "planet": 4},
    {"radius": 0.1, "distance": 1.0, "speed": 0.6, "planet": 4},
    {"radius": 0.3, "distance": 1.0, "speed": 0.1, "planet": 5},
    {"radius": 0.3, "distance": 1.2, "speed": 0.1, "planet": 5},
    {"radius": 0.4, "distance": 1.5, "speed": 0.05, "planet": 6},
]


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


def draw_sphere(radius, color):
    glColor3f(*color)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 32, 32)
    gluDeleteQuadric(quadric)


def setup_sun():
    glPushMatrix()
    emission_color = [1, 1.0, 0.0, 1.0]  # Желтый цвет (RGBA)
    glMaterialfv(GL_FRONT, GL_EMISSION, emission_color)
    draw_sphere(3.0, (1.0, 1.0, 0.0))
    glPopMatrix()


# Функция для настройки света
def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    light_position = [0, 0, 0, 1]
    light_color = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_color)


# Основная функция
def main():
    init_pygame(800, 600)

    init_opengl(800, 600)

    gluLookAt(25, 25, 25, 0, 0, 0, 0, 1, 0)

    # Установка света
    setup_lighting()

    clock = pygame.time.Clock()
    time = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Рисуем Солнце
        setup_sun()

        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

        # Рисуем планеты
        for i, planet in enumerate(PLANETS):
            angle = time * planet["speed"]
            x = planet["distance"] * math.cos(angle)
            z = planet["distance"] * math.sin(angle)

            glPushMatrix()
            glTranslatef(x, 0, z)
            draw_sphere(planet["radius"], planet["color"])

            # Рисуем спутники планет
            for moon in MOONS:
                if moon["planet"] == i:
                    moon_angle = time * moon["speed"]
                    moon_x = moon["distance"] * math.cos(moon_angle)
                    moon_z = moon["distance"] * math.sin(moon_angle)

                    glPushMatrix()
                    glTranslatef(moon_x, 0, moon_z)
                    draw_sphere(moon["radius"], (0.5, 0.5, 0.5))
                    glPopMatrix()

            glPopMatrix()

        pygame.display.flip()
        clock.tick(FPS)
        time += 1 / FPS


if __name__ == "__main__":
    main()

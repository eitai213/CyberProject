
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective

"""
rotation_angle = 0
position = [0, 0, 0]  # נקודת המיקום של הדמות
"""

def vertices_cube(x):
    vertices_cubee = (
        (x, -x, -x),
        (x, x, -x),
        (-x, x, -x),
        (-x, -x, -x),
        (x, -x, x),
        (x, x, x),
        (-x, -x, x),
        (-x, x, x)
    )
    return vertices_cubee

def create_cube_edges():
    edges = []
    num1 = 0
    while num1 < 8:
        num2 = 0
        while num2 < 8:
            if num1 != num2:
                edges.append([num1, num2])
            num2 += 1
        num1 += 1
    return edges



def draw_cube(vertices):
    edges = create_cube_edges()
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def add_cube(vertices_cube=vertices_cube(x=0.3), a=0, b=0, c=0):
    edges = create_cube_edges()
    vertices = [
        (x + 2*a, y + 2*b, z + 2*c) for x, y, z in vertices_cube]
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()



def draw_humen(position ,rotation_angle):
    a = 0.2
    body = vertices_cube(a)
    hands = vertices_cube(0.1)
    hed = vertices_cube(0.15)
    glTranslatef(position[0], position[1], position[2])
    glRotatef(rotation_angle, 0, 1, 0)
    draw_cube(body)
    add_cube(body, b=a)
    add_cube(hands, a=-a, b=a)
    add_cube(hands, a=a, b=a)
    add_cube(hands, a=a*0.5, b=-a)
    add_cube(hands, a=-a*0.5, b=-a)
    add_cube(hed, b=2*a)
    glRotatef(-rotation_angle, 0, 1, 0)
    glTranslatef(-position[0], -position[1], -position[2])



def draw_floor():
    glColor3fv((0.5, 0.5, 0.5))
    glBegin(GL_LINES)
    for i in range(-10, 11):
        glVertex3f(i, -1, -10)
        glVertex3f(i, -1, 10)
        glVertex3f(-10, -1, i)
        glVertex3f(10, -1, i)
    glEnd()



def move(player):
    position = player.position
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        position[0] += 0.1
    if keys[pygame.K_LEFT]:
        position[0] -= 0.1
    if keys[pygame.K_DOWN]:
        position[2] += 0.1
    if keys[pygame.K_UP]:
        position[2] -= 0.1

    position = player.position

    # וודא שהאיש לא ישאר מחוץ לחלון
    if position[0] > 2:
        position[0] = 2
    elif position[0] < -2:
        position[0] = -2
    if position[2] > 2:
        position[2] = 2
    elif position[2] < -2:
        position[2] = -2


def update_other_players(data_players, player_num):
    i = 0
    while i < len(data_players):
        if i != player_num:
            position = data_players[i].get_position()
            rotation_angle = data_players[i].get_rotation_angle()
            draw_humen(position, rotation_angle)
        i += 1




def game(player):
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('CUBE GAME')

    gluPerspective(45, (display[0] / display[1]), 0.1, 10.0)
    glTranslatef(0, 0, -5)



    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        move(player)


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_floor()
        draw_humen(player.get_position(), player.get_rotation_angle())
        #update_other_players(data_players, player.get_player_num())

        pygame.display.flip()
        clock.tick(50)



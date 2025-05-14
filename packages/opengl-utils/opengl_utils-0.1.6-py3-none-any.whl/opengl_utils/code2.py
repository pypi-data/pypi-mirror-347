from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

def rectangle(x1,y1,x2,y2,x3,y3,x4,y4,r,g,b):
    glColor3f(r,g,b)
    glBegin(GL_QUADS)
    glVertex2f(x1,y1); glVertex2f(x2,y2)
    glVertex2f(x3,y3); glVertex2f(x4,y4)
    glEnd()

def circle(radius,r,g,b):
    glColor3f(r,g,b)
    glBegin(GL_POLYGON)
    for i in range(100):
        a = 2*math.pi*i/100
        glVertex2f(radius*math.cos(a), radius*math.sin(a))
    glEnd()

def triangle(x1,y1,x2,y2,x3,y3,r,g,b):
    glColor3f(r,g,b)
    glBegin(GL_TRIANGLES)
    glVertex2f(x1,y1); glVertex2f(x2,y2); glVertex2f(x3,y3)
    glEnd()

def line(x1,y1,x2,y2,r,g,b):
    glColor3f(r,g,b)
    glBegin(GL_LINES)
    glVertex2f(x1,y1); glVertex2f(x2,y2)
    glEnd()

tree_dx, tree_dy = 0, 0   
STEP = 20            

def draw_exam():
    rectangle(0,0,0,400,800,400,800,0, 0.49,0.99,0.0)

    glPushMatrix()
    glTranslatef(700,700,0)
    circle(50, 1.0,0.87,0.0)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(tree_dx, tree_dy, 0)
    rectangle(100,150,100,450,150,450,150,150, 0.31,0.20,0.08)
    glPushMatrix()
    glTranslatef(125,500,0)
    circle(100, 0.33,0.42,0.18)
    glPopMatrix()
    glPopMatrix()

    rectangle(250,100,250,450,650,450,650,100, 0.96,0.96,0.92)
    triangle(250,450,650,450,450,700, 0.65,0.16,0.16)
 
    rectangle(300,400,400,400,400,300,300,300, 0.24,0.24,0.24)
    rectangle(600,400,500,400,500,300,600,300, 0.24,0.24,0.24)
    line(600,350,500,350,1,1,1); line(550,400,550,300,1,1,1)
    line(300,350,400,350,1,1,1); line(350,400,350,300,1,1,1)

    rectangle(400,100,500,100,500,250,400,250, 0.40,0.26,0.13)

    glPushMatrix()
    glTranslatef(490,175,0)
    circle(10, 0,0.6,0)
    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_exam()
    glFlush()

def keyboard(key, x, y):
    global tree_dx, tree_dy
    step = STEP
    if key == b'w':   
        tree_dy += step
    elif key == b's':   
        tree_dy -= step
    elif key == b'a':    
        tree_dx -= step
    elif key == b'd':   
        tree_dx += step
    glutPostRedisplay()

def special(key, x, y):   
    global tree_dx, tree_dy
    step = STEP
    if key == GLUT_KEY_UP:
        tree_dy += step
    elif key == GLUT_KEY_DOWN:
        tree_dy -= step
    elif key == GLUT_KEY_LEFT:
        tree_dx -= step
    elif key == GLUT_KEY_RIGHT:
        tree_dx += step
    glutPostRedisplay()

def init():
    glClearColor(0.53,0.81,0.92,1)
    gluOrtho2D(0, 800, 0, 800)

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutCreateWindow(b"Move The Tree")
init()

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)  
glutSpecialFunc(special)  

glutMainLoop()
from turtle import *


def bresenham_circle(r):
    pk = 3 - 2 * r
    xk = 0
    yk = r
    points = [(xk,yk)]
    while (xk < yk):
        if (pk<0):
            xk = xk + 1
            pk = pk + 4 * xk + 6
        elif (pk>=0):
            xk = xk + 1
            yk = yk - 1
            pk = pk + 4 * (xk - yk) + 10
        if (xk != yk):
            points.append((xk,yk))
    return points

def midpoint_circle(r):
    pk = 1 - r
    xk = 0
    yk = r
    points = [(xk, yk)]
    while (xk < yk):
        if pk >= 0:
            xk = xk + 1
            yk = yk - 1 
            pk = pk + 2 * (xk - yk) + 1
        elif pk < 0:
            xk = xk + 1
            yk = yk 
            pk = pk + 2 * (xk) + 1
        if (xk != yk):
            points.append((xk, yk))
    return points


x0 , y0 = 100, 100
octant1 = bresenham_circle(90)
octant2 = [(y, x) for x, y in octant1]
octant3 = [(-x, y) for x, y in octant1]
octant4 = [(-y, x) for x, y in octant1]
octant5 = [(-x, -y) for x, y in octant1]
octant6 = [(-y, -x) for x, y in octant1]
octant7 = [(x, -y) for x, y in octant1]
octant8 = [(y, -x) for x, y in octant1]

circle_octants = [octant1, octant2, octant3, octant4, octant5, octant6, octant7, octant8]
circle_quadrants = [
    octant1 + octant2,
    octant3 + octant4,
    octant5 + octant6,
    octant7 + octant8
]

print("Circle Octants")
for i in range(len(circle_octants)):
    print(f"Octant {i+1}")
    print(circle_octants[i])

print(50 * "#")

print("Circle Octants")
for i in range(len(circle_quadrants)):
    print(f"Quadrant {i+1}")
    print(circle_quadrants[i])

t = Turtle()
t.speed(0)
t.penup()

for octant in circle_quadrants:
    for x, y in octant:
        t.goto(x + x0, y + y0)
        t.dot(3, "black")

t. goto(x0-70, y0)
t.pendown()
t.pensize(5)
t.write("Tawfiq Bhyry", font=("Rubik", 12, "bold"))

t.hideturtle()
done()

def bresenham_line(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    pk = 2 * dy - dx
    xk = x0
    yk = y0
    points.append((xk,yk))
    for _ in range(xk + 1):
        if pk < 0:
            xk = xk + 1
            pk = pk + 2 * dy
        elif pk >= 0:
            xk = xk + 1
            yk = yk + 1
            pk = pk + 2 * (dy - dx)
        points.append((xk,yk))
    return points


def midpoint_line(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    d = 2 * dy - dx
    delta_d = 2 * (dy - dx)
    xk = x0
    yk = y0
    points.append((xk,yk))
    for _ in range(xk + 1):
        if d < 0:
            xk = xk + 1
            d = d + (2 * dx)
        elif d >= 0:
            xk = xk + 1
            yk = yk + 1
            d = delta_d
        points.append((xk,yk))
    return points



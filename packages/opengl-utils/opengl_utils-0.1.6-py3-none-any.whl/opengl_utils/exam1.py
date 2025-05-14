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


def translate(points, tx, ty):
    translated = [(x + tx, y + ty) for x, y in points]
    return translated

def rotate(points, angle):
    from math import radians, sin, cos
    rad = radians(angle)
    cos_val, sin_val = cos(rad), sin(rad)
    rotated = []
    for x, y in points:
        rotated.append((
            x * cos_val - y * sin_val,
            x * sin_val + y * cos_val
        ))
    return rotated

def scale(points, sx, sy):
    scaled = []
    for x, y in points:
        scaled.append((x * sx, y * sy))
    return scaled


from turtle import *

t = Turtle()

pts = bresenham_line(100,200,200,300)

t.penup()
print(pts)
for x,y in pts:
    t.goto(x,y)
    t.dot(3,'black')


new = rotate(pts, 90)

t.penup()
for x,y in new:
    t.goto(x,y)
    t.dot(3,'black')

done()
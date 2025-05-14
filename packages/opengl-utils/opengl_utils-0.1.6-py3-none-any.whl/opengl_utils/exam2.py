from turtle import *

def main():

    t = Turtle()
    t.shape('turtle')
    t.fillcolor('green')
    t.color('blue')
    t.pensize(5)
    t.speed(2)
    t.circle(100,steps=8)
    t.penup()
    t.left(90)
    t.forward(100)
    t.pendown()
    for _ in range(7):
        t.left(130)
        t.forward(30)
        t.left(50)
        t.forward(30)
        t.left(130)
        t.forward(30)
        t.left(50)
        t.forward(30)
        t.left(51)
    t.right(120)
    t.penup()
    t.forward(100)
    t.pendown()
    for _ in range(7):
        t.left(130)
        t.forward(30)
        t.left(50)
        t.forward(30)
        t.left(130)
        t.forward(30)
        t.left(50)
        t.forward(30)
        t.left(51)


    t.color('black')
    t.pensize(10)
    t.left(50)
    t.penup()
    t.forward(55)
    t.left(80)
    t.pd()

    t.forward(100)
    t.right(90)
    t.forward(100)
    t.backward(100)
    t.right(90)
    t.forward(100)
    t.left(90)
    t.forward(100)
    t.backward(100)
    t.right(90)
    t.forward(100)
    t.left(90)
    t.forward(100)
    done()




main()